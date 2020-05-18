import requests
import time


offers = {}
fees = {}
exchanges = ['CoinbasePro', 'Gemini', 'Bittrex', 'BinanceUS']
currencies = ['BTC', 'LTC', 'ETH', 'BCH']
wallet = 1000.0


def algorithm():
    global offers
    for currency in currencies:
        offers = {}
        if request_data(currency):
            update_wallet(currency)
        else:
            print("Error while request api data")
        time.sleep(24)


def request_data(currency):
    for exchange in exchanges:
        if not request_order_books(exchange, currency):
            return False
    return True


def request_order_books(exchange, currency):
    try:
        request = requests.get(
            "https://dev-api.shrimpy.io/v1/orderbooks?exchange="
            + f"{exchange}&baseSymbol={currency}&quoteSymbol=USD&limit=1"
        )
        trades = request.json()
        if "error" not in trades:
            offers[exchange] = {
                'asks': trades[0]['orderBooks'][0]['orderBook']['asks'][0],
                'bids': trades[0]['orderBooks'][0]['orderBook']['bids'][0]
            }
            return True
    except requests.exceptions.RequestException:
        offers[exchange] = None
    return False


def update_wallet(currency):
    global wallet
    result = calculate_profit()
    if result['profit'] > 0:
        wallet += result['profit']
        print(
            f"Bought {result['quantity']} of {currency} "
            + f"with rate of {result['buy_value']} "
            + f"from {result['buy_exchange']} "
            + f"and sold it at {result['sell_exchange']} "
            + f"with rate of {result['sell_value']} "
            + f"with total profit of {result['profit']:>0.6f} USD"
        )
    else:
        print(f"Unprofitable transaction with {currency}")
    print(f"Wallet : {wallet} USD")


def calculate_profit():
    global offers
    for exchange in exchanges:
        offers[exchange]['asks']['price'] = float(offers[exchange]['asks']['price']) * (fees[exchange] + 1)
        offers[exchange]['bids']['price'] = float(offers[exchange]['bids']['price']) * (1 - fees[exchange])
    (buy_exchange, sell_exchange) = get_best_exchanges()
    buy_value = float(offers[buy_exchange]['asks']['price'])
    sell_value = float(offers[sell_exchange]['bids']['price'])
    quantity = min(
        float(offers[buy_exchange]['asks']['quantity']),
        float(offers[sell_exchange]['bids']['quantity']),
        wallet / buy_value
    )
    profit = sell_value - buy_value
    profit *= quantity
    return {
        'quantity': quantity,
        'buy_value': buy_value,
        'buy_exchange': buy_exchange,
        'sell_value': sell_value,
        'sell_exchange': sell_exchange,
        'profit': profit
    }


def get_best_exchanges():
    best_buy_exchange = exchanges[0]
    best_sell_exchange = exchanges[0]
    for i in range(1, len(exchanges)):
        if offers[exchanges[i]]['asks']['price'] < offers[best_buy_exchange]['asks']['price']:
            best_buy_exchange = exchanges[i]
        if offers[exchanges[i]]['bids']['price'] > offers[best_sell_exchange]['bids']['price']:
            best_sell_exchange = exchanges[i]
    return best_buy_exchange, best_sell_exchange


def fetch_fee():
    global fees
    try:
        request = requests.get("https://dev-api.shrimpy.io/v1/list_exchanges")
        unparsed_fees = request.json()
        for market in unparsed_fees:
            for exchange in exchanges:
                if market["exchange"] == exchange.lower():
                    fees[exchange] = market["worstCaseFee"]
    except requests.exceptions.RequestException:
        return False
    return True


def main():
    if fetch_fee():
        algorithm()
    else:
        print("Error while fetching fees")


if __name__ == '__main__':
    main()