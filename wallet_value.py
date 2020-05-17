import requests
import sqlite3
import tkinter
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog
import os
from create_database import create_database

database_name = "database.db"
base_currency = None
wallet = {}
sources = {}
save_filetypes = [('database', '.db')]

window = tkinter.Tk()
wallet_display = tkinter.StringVar(value="Empty wallet")


def calculate_wallet_value():
    total_value = 0
    for key in wallet:
        value = get_value(base_currency, key, wallet[key])
        total_value += value
    return total_value


def get_orderbook(base_currency, currency, source):
    if source == 'bittrex':
        orderbook = requests.get(
            "https://api.bittrex.com/api/v1.1/public/getorderbook?market={0}-{1}&type=sell".format(base_currency,
                                                                                                   currency))
        orderbook_json = orderbook.json()
        orderbook_result = []
        for dict in orderbook_json['result']:
            orderbook_result.append([dict['Rate'], dict['Quantity']])
        return orderbook_result
    elif source == 'bitbay':
        orderbook = requests.get("https://bitbay.net/API/Public/{0}{1}/orderbook.json".format(currency, base_currency))
        return orderbook.json()['asks']
    else:
        return None


def get_value(base_currency, currency, amount):
    orderbook = get_orderbook(base_currency, currency, sources[(base_currency, currency)])
    # print(orderbook_json['result'])
    total_value = 0
    amount_left = amount
    current_index = 0
    while amount_left > 0:
        quantity = orderbook[current_index][1]
        rate = orderbook[current_index][0]
        if quantity >= amount_left:
            total_value += amount_left * rate
            amount_left = 0
        else:
            total_value += quantity * rate
            amount_left -= quantity
        current_index += 1
    return total_value


def calculate_wallet_value_dialog():
    messagebox.showinfo("Information",
                        "Value of your wallet in {0} is: {1}".format(base_currency, calculate_wallet_value()))


def set_base_currency(currency):
    global base_currency
    base_currency = currency


def check_market_availability(base_currency, currency):
    available = False
    orderbook = requests.get(
        "https://api.bittrex.com/api/v1.1/public/getorderbook?market={0}-{1}&type=both".format(base_currency, currency))
    orderbook_json = orderbook.json()
    if orderbook_json['success']:
        available = True
        sources[(base_currency, currency)] = "bittrex"
    if not available:
        orderbook = requests.get("https://bitbay.net/API/Public/{0}{1}/orderbook.json".format(currency, base_currency))
        orderbook_json = orderbook.json()
        if 'bids' in orderbook_json.keys():
            available = True
            sources[(base_currency, currency)] = "bitbay"
    return available


def add_wallet_data(currency, amount):
    if check_market_availability(base_currency, currency):
        if currency in wallet.keys():
            wallet[currency] += amount
        else:
            wallet[currency] = amount
    else:
        messagebox.showerror("Error", "{0}-{1} market isn't available".format(base_currency, currency))


def add_wallet_data_dialog():
    currency_name = simpledialog.askstring("Input", "Enter the currency name",
                                           parent=window)
    amount = simpledialog.askfloat("Input", "Enter the currency amount to add",
                                   parent=window)
    add_wallet_data(currency_name, amount)
    update_wallet_display()


def set_wallet_data(currency, amount):
    if check_market_availability(base_currency, currency):
        wallet[currency] = amount
    else:
        messagebox.showerror("Error", "{0}-{1} market isn't available".format(base_currency, currency))


def set_wallet_data_dialog():
    currency_name = simpledialog.askstring("Input", "Enter the currency name",
                                           parent=window)
    amount = simpledialog.askfloat("Input", "Enter the currency amount to set",
                                   parent=window)
    set_wallet_data(currency_name, amount)
    update_wallet_display()


def delete_wallet_data(currency):
    if currency in wallet.keys():
        wallet.pop(currency, None)
    else:
        messagebox.showerror("Error", "{0} isn't in your wallet".format(currency))


def delete_wallet_data_dialog():
    currency_name = simpledialog.askstring("Input", "Enter the currency name to delete",
                                           parent=window)
    delete_wallet_data(currency_name)
    update_wallet_display()


def load_data(filename):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM wallet_data")
    rows = cursor.fetchall()
    for row in rows:
        wallet[row[0]] = row[1]
    cursor.execute("SELECT * FROM currency_data")
    rows = cursor.fetchall()
    set_base_currency(rows[0][0])
    for row in rows:
        sources[(row[0], row[1])] = row[2]
    connection.commit()
    connection.close()


def load_wallet_dialog():
    answer = filedialog.askopenfilename(parent=window,
                                        initialdir=os.getcwd(),
                                        title="Please select a save file:",
                                        filetypes=save_filetypes)
    load_data(answer)
    update_wallet_display()


def save_data(filename):
    create_database(filename)
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM wallet_data")
    cursor.execute("DELETE FROM currency_data")
    for key in wallet:
        cursor.execute("INSERT INTO wallet_data VALUES (?,?)",
                       (key, wallet[key]))
    for key in sources:
        cursor.execute("INSERT INTO currency_data VALUES (?,?,?)",
                       (key[0], key[1], sources[key]))
    connection.commit()
    connection.close()


def save_wallet_dialog():
    answer = filedialog.asksaveasfilename(parent=window,
                                          initialdir=os.getcwd(),
                                          title="Please select a file name for saving:",
                                          filetypes=save_filetypes)
    save_data(answer + ".db")


def update_wallet_display():
    display_text = "Currency: Amount\n"
    for key in wallet:
        display_text += "{0}: {1}\n".format(key, wallet[key])
    wallet_display.set(display_text)


def create_main_window():
    window.geometry("250x300")
    window.title("Wallet")
    answer = messagebox.askyesno("Question", "Do you want to load a wallet?")
    if answer:
        load_wallet_dialog()
    else:
        currency_answer = simpledialog.askstring("Input", "Enter the base currency of your wallet",
                                                 parent=window)
        set_base_currency(currency_answer)
    label = tkinter.Label(window, text="Your wallet (base currency - {0})".format(base_currency))
    enter_currency_button = tkinter.Button(window, text="Enter currency amount", command=add_wallet_data_dialog)
    adjust_currency_button = tkinter.Button(window, text="Adjust currency amount", command=set_wallet_data_dialog)
    delete_currency_button = tkinter.Button(window, text="Delete currency", command=delete_wallet_data_dialog)
    calculate_value_button = tkinter.Button(window, text="Calculate value", command=calculate_wallet_value_dialog)
    save_button = tkinter.Button(window, text="Save wallet", command=save_wallet_dialog)
    wallet_data_display = tkinter.Label(window, textvariable=wallet_display)
    exit_button = tkinter.Button(window, text="Quit", command=window.quit)
    label.pack()
    enter_currency_button.pack()
    adjust_currency_button.pack()
    delete_currency_button.pack()
    calculate_value_button.pack()
    save_button.pack()
    wallet_data_display.pack()
    exit_button.pack(side="bottom")


def main():
    create_main_window()
    window.mainloop()


if __name__ == "__main__":
    main()
