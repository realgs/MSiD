import requests
import sys
import virualBuget
from time import sleep

budget = virualBuget.VirtualBudget(100)

exchanges = [
    'bitbay',
    'bitfinex',
    'bittrex',
    'bitstamp'
]

exchange_urls = {
    'bitbay': "https://api.bitbay.net/rest/trading/ticker/",
    'bitfinex': "https://api-pub.bitfinex.com/v2/ticker/",
    'bittrex': "https://api.bittrex.com/api/v1.1/public/getticker?market=",
    'bitstamp': "https://www.bitstamp.net/api/v2/ticker/"
}

trading_pairs = [
    "BTC for USD",
    "LTC for USD",
    "ETH for USD",
    "XRP for USD"
]

exchange_pairs = {
    'bitbay': [
        "BTC-USD",
        "LTC-USD",
        "ETH-USD",
        "XRP-USD"
    ],
    'bitfinex': [
        "tBTCUSD",
        "tLTCUSD",
        "tETHUSD",
        "tXRPUSD"
    ],
    'bittrex': [
        "USD-BTC",
        "USD-LTC",
        "USD-ETH",
        "USD-XRP"
    ],
    'bitstamp': [
        "btcusd",
        "ltcusd",
        "ethusd",
        "xrpusd"
    ]
}

fees = {
    'bitbay': 0.001,
    'bitfinex': 0.002,
    'bittrex': 0.002,
    'bitstamp': 0.005
}


def get_data(url):
    headers = {'content-type': 'application/json'}

    response = requests.request("GET", url, headers=headers)
    return response.json()


def get_sells_and_buys(exchange, pair_index):
    data = get_data(exchange_urls[exchange] + exchange_pairs[exchange][pair_index])
    bid_ask_pair = None
    if exchange == 'bitbay':
        bid_ask_pair = float(data['ticker']['highestBid']), float(data['ticker']['lowestAsk'])
    if exchange == 'bitfinex':
        bid_ask_pair = data[0], data[2]
    if exchange == 'bittrex':
        bid_ask_pair = data['result']['Bid'], data['result']['Ask']
    if exchange == 'bitstamp':
        bid_ask_pair = float(data['bid']), float(data['ask'])
    return bid_ask_pair


def get_current_currency_value(exchange, pair_index):
    (bid, ask) = get_sells_and_buys(exchange, pair_index)
    return (bid + ask) / 2


def consider_commisons(exchange, bid_ask):
    bid, ask = bid_ask
    bid_ask = bid * (1 - fees[exchange]), ask * (1 + fees[exchange])
    return bid_ask


def look_for_arbitration(commisions=True):
    for pair_index in range(4):
        highestBid = 0
        lowestAsk = sys.maxsize
        bid_exchange = None
        ask_exchange = None
        for exchange in exchanges:
            if commisions:
                (bid, ask) = consider_commisons(exchange, get_sells_and_buys(exchange, pair_index))
            else:
                (bid, ask) = get_sells_and_buys(exchange, pair_index)
            if bid > highestBid:
                highestBid = bid
                bid_exchange = exchange
            if ask < lowestAsk:
                lowestAsk = ask
                ask_exchange = exchange

        diff = round(highestBid - lowestAsk, 2)
        if diff > 0:
            budget.make_transaction(lowestAsk, highestBid)
            print(f"On exchange {ask_exchange} you can buy 1 {trading_pairs[pair_index]} for {lowestAsk} and sell "
                  f"on exchange {bid_exchange} for {highestBid} making total profit of {diff} "
                  f"USD")


def printstuff():
    for exchange in exchanges:
        for pair in range(0, 4):
            print(f"{exchange}, {exchange_pairs[exchange][pair]}:")
            print(get_sells_and_buys(exchange, pair))


if __name__ == '__main__':
    while True:
        look_for_arbitration(commisions=True)
        print(budget.currentMoney)
