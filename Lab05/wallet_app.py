import json

import requests

base_currency = None
wallet_file = "wallet.json"


def load_json():
    with open(wallet_file) as f:
        return json.load(f)


def write_json(data):
    """Write a given data to the file"""
    with open(wallet_file, 'w') as f:
        json.dump(data, f, indent=4)


def create_json():
    write_json({'currencies': {}})


def get_bitbay_orderbook(currency0, currency1):
    market = (currency0 + currency1).upper()
    url = f'https://bitbay.net/API/Public/{market}/orderbook.json'
    orderbook = requests.get(url).json()
    return orderbook


def is_market_available(currency):
    orderbook = get_bitbay_orderbook(base_currency, currency)
    if 'bids' in orderbook.keys():
        return True
    return False


def add_currency(currency, amount):
    if is_market_available(currency):
        wallet = load_json()
        if currency in wallet["currencies"]:
            wallet["currencies"][currency] += amount
        else:
            wallet["currencies"][currency] = amount
        write_json(wallet)


def remove_currency(currency, amount):
    wallet = load_json()
    if currency in wallet["currencies"]:
        wallet["currencies"][currency] -= amount
        if wallet["currencies"][currency] <= 0:
            del wallet["currencies"][currency]
    write_json(wallet)


def update_currency(currency, amount):
    wallet = load_json()
    if currency in wallet["currencies"]:
        wallet["currencies"][currency] = amount
    write_json(wallet)
