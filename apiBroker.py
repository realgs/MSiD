import requests

"""api: https://docs.bitbay.net/v1.0.1-en/reference """

baseCurrencies = [
    'PLN',
    'EUR',
    'USD',
    'BTC',
    'USDC',
    'GBP'
]


def get_markets():
    markets = []
    url = f"https://api.bitbay.net/rest/trading/ticker"
    headers = {'content-type': 'application/json'}

    data = requests.request("GET", url, headers=headers).json()
    for item in data['items']:
        markets.append(item)
    return markets


def api_supports_resource(resource):
    markets = get_markets()
    for trading_pair in markets:
        currency = trading_pair.split('-')[0]
        if currency == resource:
            return True
    return False


def getBuyOrders(currency, resource):
    url = f"https://api.bitbay.net/rest/trading/orderbook/{resource}-{currency}"

    headers = {'content-type': 'application/json'}

    response = requests.request("GET", url, headers=headers).json()

    if response['status'] == 'Fail':
        return None
    else:
        buys = sorted(response['buy'], key=lambda dict: float(dict['ra']), reverse=True)
        return buys


def evalValue(currency, resource, amount, consider_fee=True):
    orderbook = getBuyOrders(currency, resource)
    if orderbook is None:
        return None
    else:
        total_value = 0
        for buys in orderbook:
            ca = float(buys['ca'])
            ra = float(buys['ra'])
            diff = ca if amount - ca >= 0 else amount
            amount -= diff
            total_value += diff * ra
            if amount == 0:
                break
        if consider_fee:
            return total_value * 0.975
        else:
            return total_value


if __name__ == '__main__':
    pass
