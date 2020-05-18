import sys
import time
import requests


fees = {'bitbay': 0.001,
        'bittrex': 0.0025,
        'bitstamp': 0.005,
        'bitfinex': 0.002}


wallet = {'USD': 100,
          'BTC': 0.5,
          'LTC': 30,
          'ETH': 5}


markets = [('BTC', 'USD'),
           ('LTC', 'BTC'),
           ('LTC', 'USD'),
           ('ETH', 'USD')]


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
    offers = apply_fees(offers)
    return offers


def apply_fees(offers):
    for offer in offers:
        offers[offer][0] -= offers[offer][0] * fees[offer]
        offers[offer][2] += offers[offer][0] * fees[offer]
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


def get_arbitrage(currency0, currency1):
    offers = get_stocks_offers(currency0, currency1)
    best_buy_stock, best_sell_stock = get_best_offers(offers)
    buy_offer = offers[best_buy_stock]
    sell_offer = offers[best_sell_stock]

    quantity = min(buy_offer[3], sell_offer[1])
    quantity = min(quantity, wallet[currency1] / buy_offer[2])
    profit = quantity * (sell_offer[0] - buy_offer[2])

    if profit > 0:
        print(f'On {best_buy_stock} you can buy {quantity} {currency0}'
              f' for {currency1} at the rate {buy_offer[2]}'
              f' and sell on {best_sell_stock} at the rate {sell_offer[0]}'
              f' to earn {profit} {currency1}')
        wallet[currency1] += profit

    return profit


def main():
    while True:
        for m in markets:
            get_arbitrage(m[0], m[1])
        print(wallet)
        time.sleep(5)


if __name__ == '__main__':
    main()
