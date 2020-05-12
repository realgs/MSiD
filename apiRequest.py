import requests


def check_if_tradable(currency_type, exchanges):
    try:
        for exchange in exchanges:
            request = requests.get(
                "https://dev-api.shrimpy.io/v1/exchanges/"
                + f"{exchange}/trading_pairs"
            )
            trading_pairs = request.json()
            if 'error' not in trading_pairs:
                for pair in trading_pairs:
                    if pair['baseTradingSymbol'] == currency_type.upper() and pair['quoteTradingSymbol'] == 'USD':
                        return True
    except requests.exceptions.RequestException:
        return False
    return False


def list_exchanges():
    try:
        request = requests.get(
            "https://dev-api.shrimpy.io/v1/list_exchanges"
        )
        exchanges_list = request.json()
        if 'error' not in exchanges_list:
            return exchanges_list
    except requests.exceptions.RequestException:
        return []
    return []


def request_order_books(exchanges, currencies):
    try:
        exchange_string = ""
        for exchange in exchanges:
            exchange_string += exchange + ","
        exchange_string = exchange_string[:-1]
        currency_string = ""
        for currency in currencies:
            currency_string += currency + ","
        currency_string = currency_string[:-1]
        request = requests.get(
            "https://dev-api.shrimpy.io/v1/orderbooks?exchange="
            + f"{exchange_string}&baseSymbol={currency_string}&quoteSymbol=USD&limit=10"
        )
        trades = request.json()
        if "error" not in trades:
            return trades
    except requests.exceptions.RequestException:
        return []
    return []
