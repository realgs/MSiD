import json
import requests

base_currency = "USD"
wallet_file = "wallet.json"


def load_json():
    with open(wallet_file) as f:
        return json.load(f)


def write_json(data):
    with open(wallet_file, 'w') as f:
        json.dump(data, f, indent=4)


def create_json():
    write_json({'currencies': {}})


def get_orderbook(currency):
    market = (currency + base_currency).upper()
    url = f'https://bitbay.net/API/Public/{market}/orderbook.json'
    orderbook = requests.get(url).json()
    return orderbook


def set_base_currency(currency):
    global base_currency
    currency = currency.upper()
    base_currency = currency


def is_market_available(currency):
    orderbook = get_orderbook(currency)
    if 'bids' in orderbook.keys():
        return True
    return False


def add_currency(currency, amount):
    currency = currency.upper()
    if is_market_available(currency):
        wallet = load_json()
        if currency in wallet["currencies"]:
            wallet["currencies"][currency] += amount
        else:
            wallet["currencies"][currency] = amount
        write_json(wallet)
        return True
    return False


def remove_currency(currency, amount):
    currency = currency.upper()
    wallet = load_json()
    if currency in wallet["currencies"]:
        wallet["currencies"][currency] -= amount
        if wallet["currencies"][currency] <= 0:
            del wallet["currencies"][currency]
        write_json(wallet)
        return True
    return False


def update_currency(currency, amount):
    currency = currency.upper()
    wallet = load_json()
    if currency in wallet["currencies"]:
        wallet["currencies"][currency] = amount
        write_json(wallet)
        return True
    return False


def get_currency_value(currency, amount):
    bids = get_orderbook(currency)['bids']
    value = 0
    index = 0
    while True:
        offer = bids[index]
        if offer[1] < amount:
            value += offer[0] * offer[1]
            amount -= offer[1]
            index += 1
        else:
            value += offer[0] * amount
            return value
        if index == len(bids):
            return -1


def get_wallet_value():
    wallet = load_json()
    value = 0
    for currency in wallet['currencies']:
        currency_value = get_currency_value(currency, wallet['currencies'][currency])
        if currency_value > 0:
            value += currency_value
    return value


def get_wallet_info():
    wallet = load_json()
    wallet_str = ''
    for currency in wallet['currencies']:
        wallet_str += f'{currency} {wallet["currencies"][currency]} ' \
                      f'({base_currency} {get_currency_value(currency, wallet["currencies"][currency])})\n'
    wallet_str += f'TOTAL: {base_currency} {get_wallet_value()}'
    return wallet_str
