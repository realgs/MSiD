import requests


bids = []
asks = []


def print_orderbook(crypto, currency):
    get_orderbook(crypto, currency)
    print('BIDS')
    for bid in bids:
        print(f'\t{bid[1]} (rate: {bid[0]})')
    print('-' * 30)
    print('ASKS')
    for ask in asks:
        print(f'\t{ask[1]} (rate: {ask[0]})')


def orderbook_url(crypto, currency):
    return f'https://bitbay.net/API/Public/{crypto}{currency}/orderbook.json'


def get_orderbook(crypto, currency):
    global bids
    global asks
    orderbook = requests.get(orderbook_url(crypto, currency)).json()
    bids = orderbook['bids']
    asks = orderbook['asks']
