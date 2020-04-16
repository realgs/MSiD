import requests
import time


def get_data(crypto, currency, category):
    url = f'https://bitbay.net/API/Public/{crypto}{currency}/{category}.json'
    return requests.get(url).json()


def print_orderbook(crypto, currency):
    orderbook = get_data(crypto, currency, 'orderbook')
    bids = orderbook['bids']
    asks = orderbook['asks']
    print(f'{crypto}-{currency}')
    print('BIDS')
    for bid in bids:
        print(f'\t{bid[1]:>-10} (rate: {bid[0]:>-10})')
    print('-' * 30)
    print('ASKS')
    for ask in asks:
        print(f'\t{ask[1]:>-10} (rate: {ask[0]:>-10})')


def get_percent_diff(bid, ask):
    return 1 - (ask - bid) / bid


def diff_monitor(crypto, currency):
    print(f'{crypto}-{currency} percentage difference')
    while True:
        data = get_data(crypto, currency, 'ticker')
        print(f'\t{get_percent_diff(data["bid"], data["ask"])}%')
        time.sleep(5)
