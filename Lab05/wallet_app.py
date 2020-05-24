import json
import requests
import os.path

base_currency = "USD"
wallet_file = "wallet.json"
currency_precision = 8


def load_json():
    if not os.path.exists(wallet_file):
        create_json()
    with open(wallet_file) as f:
        return json.load(f)


def write_json(data):
    with open(wallet_file, 'w') as f:
        json.dump(data, f, indent=4)


def create_json():
    write_json({'currencies': {}})


def get_bids(currency):
    bids = []

    # bitbay
    market = (currency + base_currency).upper()
    url = f'https://bitbay.net/API/Public/{market}/orderbook.json'
    orderbook = requests.get(url).json()
    if 'bids' in orderbook.keys():
        bids = orderbook['bids']

    # bittrex
    market = (base_currency + '-' + currency).upper()
    url = f'https://api.bittrex.com/api/v1.1/public/getorderbook?market={market}&type=both'
    orderbook = requests.get(url).json()
    if orderbook['success'] == 'true':
        orderbook = orderbook['result']['buy']
        for i in range(orderbook):
            bids.append([orderbook[i]['Rate'], orderbook[i]['Quantity']])

    bids.sort()
    bids.reverse()
    print(bids)
    return bids


def set_base_currency(currency):
    global base_currency
    currency = currency.upper()
    base_currency = currency


def is_market_available(bids):
    if bids:
        return True
    return False


def add_currency(currency, amount):
    currency = currency.upper()
    bids = get_bids(currency)
    if is_market_available(bids):
        wallet = load_json()
        if currency in wallet["currencies"]:
            wallet["currencies"][currency] = round(wallet["currencies"][currency] + amount, currency_precision)
        else:
            wallet["currencies"][currency] = round(amount, currency_precision)
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
    amount = round(amount, currency_precision)
    wallet = load_json()
    if currency in wallet["currencies"]:
        wallet["currencies"][currency] = amount
        write_json(wallet)
        return True
    return False


def get_currency_value(currency, amount):
    currency = currency.upper()
    if currency == base_currency:
        return amount
    bids = get_bids(currency)
    if is_market_available(bids):
        value = 0
        index = 0
        while True:
            offer = bids[index]
            if offer[1] < amount:
                value = round(value + offer[0] * offer[1], currency_precision)
                amount -= offer[1]
                index += 1
            else:
                value = round(value + offer[0] * amount, currency_precision)
                return value
            if index == len(bids):
                # if amount is too big
                return -1
    # if market isn't available
    return -2


def get_wallet_value():
    wallet = load_json()
    total_value = 0
    for currency in wallet['currencies']:
        currency_value = get_currency_value(currency, wallet['currencies'][currency])
        if currency_value > 0:
            total_value = round(total_value + currency_value, currency_precision)
    return total_value


def get_wallet_info():
    wallet = load_json()
    wallet_str = ''
    total_value = 0
    for currency in wallet['currencies']:
        amount = wallet["currencies"][currency]
        value = get_currency_value(currency, amount)
        # if market is available
        if value != -2:
            wallet_str += f'{currency} {amount}'
            if value == -1:
                wallet_str += ' (too big amount - not count)\n'
            else:
                wallet_str += f' ({base_currency} {value})\n'
                total_value = round(total_value + value, currency_precision)
    wallet_str += f'\nTOTAL: {base_currency} {total_value}'
    return wallet_str
