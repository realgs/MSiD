import requests
from time import sleep

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

budget = {
    'USD': 1000.0,
    'BTC': 0.1,
    'LTC': 20.0,
    'XRP': 4500.0,
    'ETH': 5.0
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
        return (data['bids'][0][0], data['bids'][0][1]),( data['asks'][0][0],data['asks'][0][1])
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
    buy = find_best_buy(buy)
    sell = find_best_sell(sell)
    quantity = min(buy[1], sell[1])
    if quantity * sell[0] > budget[market[1]]:
        quantity = budget[market[1]] / sell[0]
    profit = quantity * (buy[0] - sell[0] - buy[0] * taker[buy[2]] - sell[0] * taker[sell[2]])
    if profit > 0:
        print(f'You can buy {quantity} of {market[0]} in {market[1]} on {sell[2]} for {sell[0]} '
              f'and sell on {buy[2]} for {buy[0]} '
              f'gaining {profit} {market[1]}')
        budget[market[1]] += profit


def calculate_best_arbitrage():
    for market in markets:
        buy = []
        sell = []
        for api in apis:
            data = get_buy_sell_list(api, market)
            buy.append(data[0]+(api,))
            sell.append(data[1]+(api,))
        get_best_arbitrage(buy, sell, market)
    print(budget)


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


if __name__ == "__main__":
    update_best_arbitrage()


