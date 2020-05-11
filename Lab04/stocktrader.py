import sys
import time
import requests


fees = {'bitbay': 0.001,
        'bittrex': 0.0025,
        'bitstamp': 0.005,
        'bitfinex': 0.002}


def get_bitbay_orderbook(currency0, currency1):
    market = (currency0 + currency1).upper()
    url = f'https://bitbay.net/API/Public/{market}/orderbook.json'
    orderbook = requests.get(url).json()
    best_offers = [orderbook['bids'][0][0],
                   orderbook['bids'][0][1],
                   orderbook['asks'][0][0],
                   orderbook['asks'][0][1]]
    return best_offers


def get_bittrex_orderbook(currency0, currency1):
    market = (currency1 + '-' + currency0).upper()
    url = f'https://api.bittrex.com/api/v1.1/public/getorderbook?market={market}&type=both'
    orderbook = requests.get(url).json()
    best_offers = [orderbook['result']['buy'][0]['Rate'],
                   orderbook['result']['buy'][0]['Quantity'],
                   orderbook['result']['sell'][0]['Rate'],
                   orderbook['result']['sell'][0]['Quantity']]
    return best_offers


def get_bitstamp_orderbook(currency0, currency1):
    market = (currency0 + currency1).lower()
    url = f'https://www.bitstamp.net/api/v2/order_book/{market}'
    orderbook = requests.get(url).json()
    best_offers = [float(orderbook['bids'][0][0]),
                   float(orderbook['bids'][0][1]),
                   float(orderbook['asks'][0][0]),
                   float(orderbook['asks'][0][1])]
    return best_offers


def get_bitfinex_orderbook(currency0, currency1):
    market = (currency0 + currency1).upper()
    url = f'https://api-pub.bitfinex.com/v2/book/t{market}/P0?len=1'
    orderbook = requests.get(url).json()
    best_offers = [orderbook[0][0],
                   orderbook[0][2],
                   orderbook[1][0],
                   orderbook[1][2] * -1]
    return best_offers


def get_stocks_offers(currency0, currency1):
    offers = {'bitbay': get_bitbay_orderbook(currency0, currency1),
              'bittrex': get_bittrex_orderbook(currency0, currency1),
              'bitstamp': get_bitstamp_orderbook(currency0, currency1),
              'bitfinex': get_bitfinex_orderbook(currency0, currency1)}
    return offers


def get_best_offers(stocks_offers):
    best_buy_price = sys.float_info.max
    best_sell_price = 0
    best_buy_stock = None
    best_sell_stock = None
    for stock in stocks_offers:
        if stocks_offers[stock][0] > best_sell_price:
            best_sell_price = stocks_offers[stock][0]
            best_sell_stock = stock
        if stocks_offers[stock][2] < best_buy_price:
            best_buy_price = stocks_offers[stock][2]
            best_buy_stock = stock
    return best_buy_stock, best_sell_stock


def check_arbitrage(currency0, currency1):
    offers = get_stocks_offers(currency0, currency1)
    best_buy_stock, best_sell_stock = get_best_offers(offers)
    quantity = min(offers[best_buy_stock][3], offers[best_sell_stock][1])
    profit = quantity * (offers[best_sell_stock][0] * (1 - fees[best_sell_stock]) -
                         offers[best_buy_stock][2] * (1 + fees[best_buy_stock]))
    if profit > 0:
        print(f'On {best_buy_stock} you can buy {quantity} {currency0}'
              f' for {currency1} at the rate {offers[best_buy_stock][2]}'
              f' and sell on {best_sell_stock} at the rate {offers[best_sell_stock][0]}'
              f' to earn {profit} {currency1}')
    # else:
    #     print(f'No profitable operation on {currency0} - {currency1} market')
    return profit


while True:
    print(check_arbitrage('btc', 'usd'))
    time.sleep(5)