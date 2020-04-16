import requests


bids = []
asks = []


def print_orderbook(crypto, currency):
    global bids
    global asks
    orderbook = requests.get(orderbook_url(crypto, currency)).json()
    bids = orderbook['bids']
    asks = orderbook['asks']
    print(bids)
    print(asks)


def orderbook_url(crypto, currency):
    return f'https://bitbay.net/API/Public/{crypto}{currency}/orderbook.json'
