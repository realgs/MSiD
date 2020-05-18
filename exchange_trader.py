# https://docs.bitfinex.com/reference
import time
import requests
import json

fees_active = True

markets = [
    ('BTC', 'USD'),
    ('LTC', 'BTC'),
    ('XRP', 'BTC'),
    ('XLM', 'BTC'),
    ('TRX', 'BTC'),
    ('ETH', 'BTC'),
    ('BAT', 'BTC'),
]

exchanges = [
    'bitfinex',
    'bitbay',
    'bittrex',
    'binance',
]

urls = {
    'bitfinex': 'https://api-pub.bitfinex.com/v2/book/t{0}{1}/P0?len=1',
    'bitbay': 'https://api.bitbay.net/rest/trading/orderbook-limited/{0}-{1}/10',
    'bittrex': 'https://api.bittrex.com/api/v1.1/public/getorderbook?market={1}-{0}&type=both',
    'binance': 'https://api.binance.com/api/v3/depth?symbol={0}{1}&limit=10',
}

wallet = {
    "USD": 2000.0,
    "BTC": 0.2,
    "LTC": 40.0,
    "XRP": 10000.0,
    "XLM": 100000.0,
    "TRX": 100000.0,
    "ETH": 10.0,
    "BAT": 10000.0,
}

taker_fees = {
    'bitfinex': 0.002,
    'bitbay': 0.0043,
    'bittrex': 0.0025,
    'binance': 0.001,
}

def get_ask_bid(exchange, market):
    url = urls[exchange].format(market[0], market[1])
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", url, headers=headers)
    dic = response.json()

    if exchange is 'bitbay' and 'sell' in dic.keys():
        return ((float(dic['sell'][0]['ra']), float(dic['sell'][0]['ca'])),
                (float(dic['buy'][0]['ra']), float(dic['buy'][0]['ca'])))
    elif exchange is 'bitfinex' and not "error" in dic:
        return ((dic[1][0], -dic[1][2]),
                (dic[0][0], dic[0][2]))
    elif exchange is 'bittrex' and 'result' in dic.keys():
        return ((dic['result']['sell'][0]['Rate'], dic['result']['sell'][0]['Quantity']),
                (dic['result']['buy'][0]['Rate'], dic['result']['buy'][0]['Quantity']))
    elif exchange is 'binance' and 'asks' in dic.keys():
        return ((float(dic['asks'][0][0]), float(dic['asks'][0][1])),
                (float(dic['bids'][0][0]), float(dic['bids'][0][1])))
    return (None, None), (None, None)

def calculate_arbitrage_profit(quantity, bid, ask):
    if fees_active:
        return quantity * ((bid[0] - ask[0]) - (bid[0] * taker_fees[bid[2]] + ask[0] * taker_fees[ask[2]]))
    else:
        return quantity * (bid[0] - ask[0])


def symulate_arbitrage(asks, bids, market):
    while True:
        ask_index = 0
        bid_index = 0

        quantity = min(asks[ask_index][1], bids[bid_index][1])
        if quantity * asks[ask_index][0] > wallet[market[1]]:
            quantity = wallet[market[1]] / asks[ask_index][0]
        asks[ask_index][1] -= quantity
        bids[bid_index][1] -= quantity

        profit = calculate_arbitrage_profit(quantity, bids[bid_index], asks[ask_index])

        if profit <= 0:
            return
        wallet[market[0]] += profit
        print("Na gieldzie {} kupiono {:.9f} {} po kursie {} {} i sprzedano na gieldzie {} po {} {} zyskując {:.9f} {}".format(
                asks[ask_index][2], quantity, market[0], asks[ask_index][0], market[1],
                bids[bid_index][2], bids[bid_index][0], market[1], profit, market[1]))
        if asks[ask_index][1] == 0:
            ask_index += 1
        if bids[bid_index][1] == 0:
            bid_index += 1

        if bid_index >= len(bids) or ask_index >= len(asks):
            return

def analyze_markets():
    while True:
        for market in markets:
            bids = []
            asks = []
            for exchange in exchanges:
                ask, bid = get_ask_bid(exchange, market)
                if ask != (None, None):
                    asks.append(list(ask + (exchange,)))
                    bids.append(list(bid + (exchange,)))
            bids.sort(reverse=True)
            asks.sort()
            symulate_arbitrage(asks, bids, market)

        print()
        print(wallet)
        print()
        time.sleep(5)


analyze_markets()
