from datetime import datetime
import json
import requests
from time import sleep

refresh_period = 5
currency_pairs = [('LTC', 'BTC'), ('ETH', 'BTC'), ('XRP', 'BTC'), ('DASH', 'BTC')]
api_names = ['bitbay', 'bittrex', 'cex', 'binance']

wallet = []


def add_currency_to_wallet(currency_name, currency_amount):
    currency_exist = False
    for currency in wallet:
        if currency[0] == currency_name:
            currency_exist = True
            currency[1] += currency_amount

    if not currency_exist:
        wallet.append([currency_name, currency_amount])


def take_currency_from_wallet(currency_name, currency_amount):
    for currency in wallet:
        if currency[0] == currency_name:
            currency[1] -= currency_amount


def get_url_data(url):
    try:
        request = requests.get(url)
        data = json.loads(request.text)
        return data
    except requests.exceptions.ConnectionError:
        print("No connection")
        return None


def create_market_url(base_currency, exchange_currency, api_name):
    base_currency = base_currency.upper()
    exchange_currency = exchange_currency.upper()

    if api_name == 'bittrex':
        return 'https://api.bittrex.com/api/v1.1/public/getorderbook?market=' + base_currency + '-' + \
               exchange_currency + "&type=both"
    if api_name == 'bitbay':
        return f'https://bitbay.net/API/Public/{base_currency}{exchange_currency}/orderbook.json'
    if api_name == 'cex':
        return f'https://cex.io/api/order_book/{base_currency}/{exchange_currency}'
    if api_name == 'binance':
        return f'https://api.binance.com/api/v3/ticker/bookTicker?symbol={base_currency}{exchange_currency}'


def get_buy_sell_data(base_currency, exchange_currency, api_name):
    data = get_url_data(create_market_url(base_currency, exchange_currency, api_name))

    buy_offers = []
    sell_offers = []

    if api_name == 'bittrex':
        for bid in data['result']['buy']:
            buy_offers.append((bid['Quantity'], bid['Rate']))
        for ask in data['result']['sell']:
            sell_offers.append((ask['Quantity'], ask['Rate']))

    if api_name == 'cex' or api_name == 'bitbay':
        for bid in data['bids']:
            buy_offers.append((bid[1], bid[0]))
        for ask in data['asks']:
            sell_offers.append((ask[1], ask[0]))

    if api_name == 'binance':
        buy_offers.append((data['bidQty'], data['bidPrice']))
        sell_offers.append((data['askQty'], data['askPrice']))

    return buy_offers, sell_offers


def get_market_fee(api_name):
    fee = 0.1

    if api_name == 'bittrex':
        fee = 0.0045
    if api_name == 'bitbay':
        fee = 0.0041
    if api_name == 'cex':
        fee = 0.0025
    if api_name == 'binance':
        fee = 0.001

    return fee


def get_wallet_currency_amount(currency_name):
    for currency in wallet:
        if currency[0] == currency_name:
            return currency[1]

    return 0


def print_wallet_state():
    print("\tWallet: ", end="| ")
    for currency in wallet:
        print(currency, end=" | ")
    print()


def search_for_arbitrage():
    for currency_pair in currency_pairs:
        markets = []

        for api in api_names:
            if api == 'bittrex':
                markets.append((get_buy_sell_data(currency_pair[1], currency_pair[0], api), api))
            else:
                markets.append((get_buy_sell_data(currency_pair[0], currency_pair[1], api), api))

        best_bid_market = ''
        best_ask_market = ''
        buy_quantity = 0
        best_profit = 0
        ask_exchange_rate = 0
        avg_exchange_rate = 0

        for market in markets:
            for ask in market[0][1]:
                currency_amount = get_wallet_currency_amount(currency_pair[1])
                quantity = float(ask[0])
                cost = (quantity * float(ask[1]))

                if currency_amount < cost:
                    quantity = currency_amount / float(ask[1])
                    cost = (quantity * float(ask[1]))

                current_quantity = quantity
                quantity *= (1 - get_market_fee(market[1]))
                for m in markets:
                    profit = 0
                    price_and_weight = []

                    highest_sell_price = float(m[0][0][0][1])
                    if float(ask[1]) < highest_sell_price:
                        for bid in m[0][0]:
                            price = float(bid[1])
                            qty = float(bid[0])
                            fee = get_market_fee(m[1])

                            if quantity >= qty:
                                profit += qty * price * (1 - fee)
                                quantity -= qty
                            else:
                                profit += ((quantity * price) / qty) * (1 - fee)
                                quantity = 0

                            price_and_weight.append((price, qty))

                            if quantity == 0:
                                if profit - cost > best_profit:
                                    best_bid_market = market[1]
                                    best_ask_market = m[1]

                                    buy_quantity = current_quantity
                                    best_profit = profit - cost
                                    ask_exchange_rate = ask[1]

                                    numerator = 0
                                    for pw in price_and_weight:
                                        numerator += pw[0] * pw[1]

                                    denominator = 0
                                    for weight in price_and_weight:
                                        denominator += weight[1]

                                    avg_exchange_rate = numerator / denominator
                                break

        print(datetime.now().strftime('[%H:%M:%S]'), end=' ')
        if best_profit <= 0 or float(ask_exchange_rate) >= avg_exchange_rate:
            print(f"Nie ma możliwości arbitrażu")
        else:
            print(f"Na giełdzie {best_ask_market} można kupić {buy_quantity} {currency_pair[0]} za {currency_pair[1]}"
                  f" po kursie {ask_exchange_rate} i sprzedać na giełdzie {best_bid_market} "
                  f"po kursie {avg_exchange_rate}, zyskując {best_profit} {currency_pair[1]}")

            for currency in wallet:
                if currency[0] == currency_pair[1]:
                    make_transaction(ask_exchange_rate, buy_quantity, avg_exchange_rate, currency_pair[0],
                                     currency_pair[1])


def buy_currency(base_currency, exchange_currency, currency_amount, bid):
    currency_amount = float(currency_amount)
    take_currency_from_wallet(base_currency, currency_amount * float(bid))
    add_currency_to_wallet(exchange_currency, currency_amount)


def sell_currency(base_currency, exchange_currency, currency_amount, bid):
    currency_amount = float(currency_amount)
    take_currency_from_wallet(base_currency, currency_amount)
    add_currency_to_wallet(exchange_currency, currency_amount * float(bid))


def make_transaction(ask_price, ask_quantity, bid_price, base_currency, exchange_currency):
    print("Buy:")
    buy_currency(exchange_currency, base_currency, ask_quantity, ask_price)
    print_wallet_state()
    print("Sell:")
    sell_currency(base_currency, exchange_currency, ask_quantity, bid_price)
    print_wallet_state()


def main():
    add_currency_to_wallet('BTC', 0.5)

    while True:
        search_for_arbitrage()
        sleep(refresh_period)


if __name__ == "__main__":
    main()
