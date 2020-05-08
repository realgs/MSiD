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

}

urls = {
    'bittrex': 'https://api.bittrex.com/api/v1.1/public/getorderbook?market={1}-{0}&type=both',
    'bitbay': 'https://bitbay.net/API/Public/{0}{1}/orderbook.json',
    'bitfinex': 'https://api-pub.bitfinex.com/v2/book/t{0}{1}/P0?len=1',
    'bitstamp': 'https://www.bitstamp.net/api/v2/order_book/{0}{1}',
}


def get_buy_sell_list(api, market):
    if api == 'bitstamp':
        url = urls[api].format(market[0].lower(), market[1].lower())
    else:
        url = urls[api].format(market[0], market[1])
    resp = requests.get(url)
    data = resp.json()
    if api == 'bittrex':
        return ((data['result']['buy'][0]['Rate'], data['result']['buy'][0]['Quantity']), (data['result']['sell'][0]['Rate'],data['result']['sell'][0]['Quantity']))
    if api == 'bitbay':
        return ((data['bids'][0][0], data['bids'][0][1]),( data['asks'][0][0],data['asks'][0][1]))
    if api == 'bitfinex':
        return ((data[0][0], data[0][2]), (data[1][0], -data[1][2]))
    if api == 'bitstamp':
        return ((data['bids'][0][0], data['bids'][0][1]), (data['asks'][0][0],data['asks'][0][1]))


#def get_best_arbitrage(data):


def arb():
    buy = []
    sell = []
    for market in markets:
        for api in apis:
            data = get_buy_sell_list(api, market)
            buy.append(data[0])
            sell.append(data[1])


#list 3
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


# print_buy_sell_list()
# print_buy_sell_percent()
# update_percent_list()
arb()


