import requests


def get_bitbay_orderbook(currency0, currency1):
    url = f'https://bitbay.net/API/Public/{currency0}{currency1}/orderbook.json'
    return requests.get(url).json()


def get_bittrex_orderbook(currency0, currency1):
    url = f'https://api.bittrex.com/api/v1.1/public/getorderbook?market={currency1}-{currency0}&type=both'
    return requests.get(url).json()


def get_bitstamp_orderbook(currency0, currency1):
    market = (currency0 + currency1).lower()
    url = f'https://www.bitstamp.net/api/v2/order_book/{market}'
    return requests.get(url).json()


def get__orderbook(currency0, currency1):
    url = f'https://api-pub.bitfinex.com/v2/book/t{currency0}{currency1}/P0'
    return requests.get(url).json()



