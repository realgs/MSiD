import requests
import json

wallet_data = {'base_currency': "", 'data': {}}

def calculate_currency_value(bids, amount):
    value = 0.0
    for bid in bids:
        rate = min(amount, bid['amount'])
        value += rate * bid['value']
        amount -= rate
        if amount == 0:
            return value

def check_currency_availability(currency):
    url = 'https://api.bittrex.com/v3/markets'
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", url, headers=headers)
    dic = response.json()
    for market in dic:
        if market['baseCurrencySymbol'] == currency:
            return True
    return False

def get_bids(currency):
    url = 'https://api.bittrex.com/api/v1.1/public/getorderbook?market={0}-{1}&type=both'.format(wallet_data['base_currency'], currency)
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", url, headers=headers)
    dic = response.json()
    if dic['success'] == True:
        bids = []
        for bid in dic['result']['sell']:
            bids.append({'amount': bid['Quantity'], 'value': bid['Rate']})
        return bids
    else:
        return None

def add_currency(currency, amount):
    bids = get_bids(currency)
    if bids is not None:
        value = calculate_currency_value(bids, amount)
        wallet_data['data'][currency] = {'amount': amount, 'value': value}
        print(wallet_data)
        return True
    return False

def remove_currency(currency, amount):
    if currency in wallet_data['data']:
        del wallet_data['data'][currency]
        return True
    return False

def set_base_currency(currency):
    if check_currency_availability(currency):
        wallet_data['base_currency'] = currency
        return True
    return False

def get_wallet_data():
    return wallet_data
