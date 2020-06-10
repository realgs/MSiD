import requests
import json

wallet_data = {'base_currency': "", 'data': {}}
database_path = "wallet.json"

markets = {
    'bitbay': 'https://api.bitbay.net/rest/trading/ticker',
    'bittrex': 'https://api.bittrex.com/v3/markets',
}

exchanges = {
    'bitbay': 'https://bitbay.net/API/Public/{0}{1}/orderbook.json',
    'bittrex': 'https://api.bittrex.com/api/v1.1/public/getorderbook?market={1}-{0}&type=both',
}

def calculate_currency_value(bids, amount):
    value = 0.0
    for bid in bids:
        rate = min(amount, bid['amount'])
        value += rate * bid['value']
        amount -= rate
        if amount == 0:
            return value

def update_currencies_values(data=wallet_data):
    for currency, cur_info in data['data'].items():
        cur_info['value'] = calculate_currency_value(get_bids(data['base_currency'], currency), cur_info['amount'])

def check_currency_availability(currency):
    for exchange, api_url in exchanges.items():
        headers = {'content-type': 'application/json'}
        response = requests.request("GET", url, headers=headers)
        dic = response.json()
        if exchange is "bitbay":
            for market in dic:
                if market['market']['first']['currency'] == currency:
                    return True
        elif exchange is 'bittrex':
            for market in dic:
                if market['baseCurrencySymbol'] == currency:
                    return True
    return False

def get_bids(base_currency, currency):
    for exchange, url in exchanges.items():
        formated_url = url.format(currency, base_currency)
        headers = {'content-type': 'application/json'}
        response = requests.request("GET", formated_url, headers=headers)
        dic = response.json()
        bids = []
        if exchange is 'bitbay' and 'bids' in dic.keys():
            for bid in dic['bids']:
                bids.append({'amount': bid[1], 'value': bid[0]})
            return bids
        elif exchange is 'bittrex' and dic['success'] == True:
            for bid in dic['result']['sell']:
                bids.append({'amount': bid['Quantity'], 'value': bid['Rate']})
            return bids
    return None

def add_currency(currency, amount):
    bids = get_bids(wallet_data['base_currency'], currency)
    if bids is not None:
        value = calculate_currency_value(bids, amount)
        wallet_data['data'][currency] = {'amount': amount, 'value': value}
        print(wallet_data)
        return True
    return False

def remove_currency(currency):
    if currency in wallet_data['data']:
        del wallet_data['data'][currency]
        return True
    return False

def change_currency_amount(currency, amount):
    if currency in wallet_data['data']:
        wallet_data['data'][currency]['amount'] += amount
        if wallet_data['data'][currency]['amount'] < 0.0:
            wallet_data['data'][currency]['amount'] = 0.0
        calculate_currency_value(get_bids(wallet_data['base_currency'], wallet_data['data'][currency]['amount']))
        return True
    return False

def set_base_currency(currency):
    if check_currency_availability(currency):
        wallet_data['base_currency'] = currency
        return True
    return False

def get_wallet_data():
    return wallet_data

def load_database():
    global wallet_data
    try:
        with open(database_path) as json_file:
            wallet_data = json.load(json_file)
            if wallet_data['base_currency'] != "":
                return True
    except OSError:
        update_database()
        return False
    return False

def update_database(data=wallet_data):
    with open(database_path, 'w') as json_file:
        json.dump(data, json_file)
