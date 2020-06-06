import requests
from time import sleep
import tkinter
from tkinter import simpledialog
from tkinter import messagebox
import sqlite3
from forex_python.bitcoin import BtcConverter

conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()
window = tkinter.Tk()
cur = BtcConverter()

markets = [
    ('BTC', 'USD'),
    ('LTC', 'BTC'),
    ('XRP', 'BTC'),
    ('ETH', 'BTC'),
]

apis = [
    'bittrex',
    'bitbay',
    'bitfinex',
    'bitstamp',
]

taker = {
    'bittrex': 0.002,
    'bitbay': 0.001,
    'bitfinex': 0.002,
    'bitstamp': 0.005,

}

urls = {
    'bittrex': 'https://api.bittrex.com/api/v1.1/public/getorderbook?market={1}-{0}&type=both',
    'bitbay': 'https://bitbay.net/API/Public/{0}{1}/orderbook.json',
    'bitfinex': 'https://api-pub.bitfinex.com/v2/book/t{0}{1}/P0?len=1',
    'bitstamp': 'https://www.bitstamp.net/api/v2/order_book/{0}{1}',
}

availableCurr = {
    'USD',
    'BTC',
    'LTC',
    'XRP',
    'ETH',
}


def get_buy_sell_list(api, market):
    if api == 'bitstamp':
        url = urls[api].format(market[0].lower(), market[1].lower())
    else:
        url = urls[api].format(market[0], market[1])
    resp = requests.get(url)
    data = resp.json()

    if api == 'bittrex':
        return (data['result']['buy'][0]['Rate'], data['result']['buy'][0]['Quantity']), (data['result']['sell'][0]['Rate'],data['result']['sell'][0]['Quantity'])
    if api == 'bitbay':
        return (data['bids'][0][0], data['bids'][0][1]), (data['asks'][0][0],data['asks'][0][1])
    if api == 'bitfinex':
        return (data[0][0], data[0][2]), (data[1][0], -data[1][2])
    if api == 'bitstamp':
        return (float(data['bids'][0][0]), float(data['bids'][0][1])), (float(data['asks'][0][0]),float(data['asks'][0][1]))


def find_best_buy(buy):
    max_b = buy[0]
    for b in buy:
        if b[0] - b[0] * taker[b[2]] > max_b[0] - max_b[0] * taker[max_b[2]]:
            max_b = b

    return max_b


def find_best_sell(sell):
    min_b = sell[0]
    for s in sell:
        if s[0] - s[0] * taker[s[2]] < min_b[0] - min_b[0] * taker[min_b[2]]:
            min_b = s

    return min_b


def get_best_arbitrage(buy, sell, market):
    wallet = get_wallet()
    buy = find_best_buy(buy)
    sell = find_best_sell(sell)
    quantity = min(buy[1], sell[1])
    budget = [m for m in wallet if m[1] == market[1]]
    if budget:
        budget_value = budget[0][2]
        if quantity * sell[0] > budget_value:
            quantity = budget_value / sell[0]
        profit = quantity * (buy[0] - sell[0] - buy[0] * taker[buy[2]] - sell[0] * taker[sell[2]])
        if profit > 0:
            messagebox.showinfo('Transaction info', f'You can buy {quantity} of {market[0]} in {market[1]} on {sell[2]} for {sell[0]} '
                f'and sell on {buy[2]} for {buy[0]} '
                f'gaining {profit} {market[1]}')
            c.execute("INSERT INTO Transactions (Quantity, MarketC, MarketC2, ApiS, AmountS, ApiB, AmountB, Profit)"
                      " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (quantity, market[0], market[1], sell[2], sell[0], buy[2], buy[0], profit))
            c.execute("UPDATE Currencies SET Amount = ? WHERE Name = ?", (budget_value+profit, market[1]))
            conn.commit()


def calculate_best_arbitrage():
    for market in markets:
        buy = []
        sell = []
        for api in apis:
            data = get_buy_sell_list(api, market)
            buy.append(data[0]+(api,))
            sell.append(data[1]+(api,))
        get_best_arbitrage(buy, sell, market)



def update_best_arbitrage():
    while True:
        calculate_best_arbitrage()
        sleep(5)


# list 3
def print_buy_sell_list():
    for market in markets:
        data = get_buy_sell_list(market)
        print(market, 'Buy', data[1], 'Sell', data[0])


def get_buy_sell_percent_diff(data):
    return 1-(data[1]-data[0])/data[0]


def print_buy_sell_percent():
    for market in markets:
        percent = get_buy_sell_percent_diff(get_buy_sell_list(market))
        print(market, percent)


def update_percent_list():
    while True:
        print_buy_sell_percent()
        sleep(5)


# list 5
def fetchall(sql):
    return c.execute(sql).fetchall()


def get_wallet():
    return fetchall("SELECT * FROM Currencies")


def get_transactions():
    return fetchall("SELECT * FROM Transactions")


def get_base_currency():
    return fetchall("SELECT * FROM Base")


def change_base_currency(labelText):
    base_currency = simpledialog.askstring("Input", "In which base currency you want your wallet?", parent=window)
    if not base_currency:
        return
    if base_currency not in availableCurr:
        messagebox.showerror('Error', f'No such currency, choose from {availableCurr}')
        change_base_currency()
        return
    if get_base_currency():
        c.execute("UPDATE Base SET Name = ? WHERE IdB = ?", (base_currency, 1))
    else:
        c.execute("INSERT INTO Base (Name) VALUES (?)", (base_currency,))
    conn.commit()
    labelText.set(f'Base currency of wallet: {base_currency}')


def create_new_wallet(labelText):
    check = messagebox.askyesno('Delete', 'Are you sure want to delete all your data?')
    if check:
        c.execute('DELETE FROM Currencies;',)
        c.execute('DELETE FROM Base;', )
        conn.commit()
        labelText.set(f'No base currency: ')


def add_currency():
    currency = simpledialog.askstring("Input", "What currency you want to add?", parent=window)
    if not currency:
        return
    if currency not in availableCurr:
        messagebox.showerror('Error', f'No such currency, choose from {availableCurr}')
        add_currency()
        return
    currency_amount = simpledialog.askinteger("Input", "How much you want to add?", parent=window)
    if not currency_amount:
        return
    c.execute("INSERT INTO Currencies (Name,Amount) VALUES (?,?)", (currency, currency_amount))
    conn.commit()


def delete_currency():
    currency = simpledialog.askstring("Input", "What currency you want to delete?", parent=window)
    if not currency:
        return
    c.execute("DELETE FROM Currencies WHERE Name=?", (currency,))
    conn.commit()


def update_currency():
    currency = simpledialog.askstring("Input", "What currency you want to change?", parent=window)
    if not currency:
        return
    currency_amount = simpledialog.askinteger("Input", "To how much amount you want to change?", parent=window)
    if not currency_amount:
        return
    c.execute("UPDATE Currencies SET Amount = ? WHERE Name = ?", (currency_amount, currency))
    conn.commit()


def calculate_values():
    c.execute("SELECT * FROM Transactions ORDER BY IdT DESC LIMIT 1")
    result = c.fetchone()
    result = list(result)
    if result:
        base = get_base_currency()
        base = base[0][1]
        if base == 'USD':
            if result[3] == 'BTC':
                result[7] = cur.convert_btc_to_cur(result[7], 'USD')
                result[8] = cur.convert_btc_to_cur(result[8], 'USD')
            if result[2] == 'BTC':
                result[5] = cur.convert_btc_to_cur(result[5], 'USD')
        elif base == 'BTC':
            if result[3] == 'USD':
                result[7] = cur.convert_to_btc(result[7], 'USD')
                result[8] = cur.convert_to_btc(result[8], 'USD')
            if result[2] == 'USD':
                result[5] = cur.convert_to_btc(result[5], 'USD')
        else:
            messagebox.showinfo('Info', 'Only converting currency USD BTC, values shown without converting')
        messagebox.showinfo(f'Last transaction values in {base}', f'You can buy {result[1]} of {result[2]} in {result[3]} on {result[4]} for {result[5]} '
                    f'and sell on {result[6]} for {result[7]} '
                    f'gaining {result[8]} {base}')
    else:
        messagebox.showerror('Error', 'No transactions available')


def print_wallet():
    print_window = tkinter.Tk()
    print_window.title('Wallet')
    data = get_wallet()
    data_labels = [[tkinter.Label(print_window, text=str(y)) for y in x] for x in data]
    for i, labels in enumerate(data_labels):
        for j, label in enumerate(labels):
            label.grid(row=i, column=j, padx=5, pady=1)

def print_transactions():
    data = get_transactions()
    if data:
        print_window = tkinter.Tk()
        print_window.title('Wallet')
        data_labels = [[tkinter.Label(print_window, text=str(y)) for y in x] for x in data]
        for i, labels in enumerate(data_labels):
            for j, label in enumerate(labels):
                label.grid(row=i, column=j, padx=5, pady=1)
    else:
        messagebox.showerror('Error', 'List of transactions empty')


def create_main_window():
    window.title('Manage your wallet')
    labelText = tkinter.StringVar()
    base_currency = get_base_currency()

    if base_currency:
        labelText.set(f'Base currency of wallet: {base_currency[0][1]}')
    else:
        labelText.set(f'No base currency: ')
    label = tkinter.Label(window, textvariable=labelText)
    buttons_data = [
        ('Change base currency', lambda: change_base_currency(labelText)),
        ('Show your wallet', print_wallet),
        ('Calculate best arbitrage', calculate_best_arbitrage()),
        ('New wallet', lambda: create_new_wallet(labelText)),
        ('Add currency', add_currency),
        ('Delete currency', delete_currency),
        ('Change currency amount', update_currency),
        ('Show all transactions', print_transactions),
        ('Calculate values of last transaction', calculate_values),
        ('Quit', window.quit),
    ]

    label.grid(pady=10)
    buttons = [tkinter.Button(window, text=b[0], command=b[1]) for b in buttons_data]

    for button in buttons:
        button.grid(sticky='nesw', padx=5)


if __name__ == "__main__":
    create_main_window()
    window.mainloop()


