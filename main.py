from datetime import datetime
import requests
from time import sleep
import sys


refresh_period = 20
currency_pairs = [('LTC', 'BTC'), ('ETH', 'BTC'), ('BTC', 'EUR'), ('XRP', 'BTC')]
api_names = ['bittrex', 'bitbay', 'bitstamp', 'cex']
wallet = [["BTC", 5], ["USD", 500]]


def get_answer(url):
    request = requests.get(url)
    answer = request.json()
    return answer


def get_orderbook_url(base_currency, wanted_currency, name):
    if name == 'bittrex':
        return 'https://api.bittrex.com/api/v1.1/public/getorderbook?market=' + base_currency + '-' + \
               wanted_currency + "&type=both"
    if name == 'bitbay':
        return 'https://bitbay.net/API/Public/' + base_currency + wanted_currency + '/orderbook.json'
    if name == 'bitstamp':
        return 'https://www.bitstamp.net/api/v2/order_book/' + base_currency + wanted_currency + '/'
    if name == 'cex':
        return f'https://cex.io/api/order_book/{base_currency}/{wanted_currency}'


def get_orderbook(base_currency, wanted_currency, name):
    answer = get_answer(get_orderbook_url(base_currency, wanted_currency, name))

    if name == 'bittrex':
        if answer['success']:
            buy = answer['result']['buy'][0]
            sell = answer['result']['sell'][0]
            result = ['bittrex', float(buy['Quantity']), float(buy['Rate']), float(sell['Quantity']),
                      float(sell['Rate'])]
            return result
    if name == 'bitbay':
        buy = answer['bids'][0]
        sell = answer['asks'][0]
        result = ['bitbay', float(buy[1]), float(buy[0]), float(sell[1]), float(sell[0])]
        return result
    if name == 'bitstamp':
        buy = answer['bids'][0]
        sell = answer['asks'][0]
        result = ['bitstamp', float(buy[1]), float(buy[0]), float(sell[1]), float(sell[0])]
        return result
    if name == 'cex':
        buy = answer['bids'][0]
        sell = answer['asks'][0]
        result = ['cex', float(buy[1]), float(buy[0]), float(sell[1]), float(sell[0])]
        return result


def get_fee(api_name):
    fee = 0.1

    if api_name == 'bittrex':
        fee = 0.0045
    if api_name == 'bitbay':
        fee = 0.0041
    if api_name == 'bitstamp':
        fee = 0.001
    if api_name == 'cex':
        fee = 0.0025

    return fee


def print_wallet_info():
    print(f'Portfel:')
    for i in range(len(wallet)):
        print(f'\t {wallet[i][0]}: {wallet[i][1]}')


def update_wallet(currency, amount):
    currency = currency.upper()
    for i in range(len(wallet)):
        if wallet[i][0] == currency:
            wallet[i][1] = float(wallet[i][1]) + amount


def get_arbitration_table(currency1, currency2, names):
    arbitration_table = []

    bittrex_orderbook = get_orderbook(currency2.upper(), currency1.upper(), names[0])
    bitbay_orderbook = get_orderbook(currency1.upper(), currency2.upper(), names[1])
    bitstamp_orderbook = get_orderbook(currency1.lower(), currency2.lower(), names[2])
    cex_orderbook = get_orderbook(currency1.upper(), currency2.upper(), names[3])
    all_orderbook = [bittrex_orderbook, bitbay_orderbook, bitstamp_orderbook, cex_orderbook]

    the_cheapest_offer_to_buy = ("Null", 0, sys.float_info.max)
    for offer_to_buy in all_orderbook:
        if offer_to_buy[4] < the_cheapest_offer_to_buy[2]:
            the_cheapest_offer_to_buy = (offer_to_buy[0], offer_to_buy[3], offer_to_buy[4])
    for offer_to_sell in all_orderbook:
        profit = check_profit(the_cheapest_offer_to_buy, offer_to_sell)
        if profit[0] > 0:
            arbitration_table.append([the_cheapest_offer_to_buy[0], profit[1], the_cheapest_offer_to_buy[2],
                                                 offer_to_sell[0], offer_to_sell[1], offer_to_sell[2], profit[0]])
    return arbitration_table


def check_profit(the_cheapest_offer_to_buy, offer_to_sell):
    if the_cheapest_offer_to_buy[1] < offer_to_sell[1]:
        amount = the_cheapest_offer_to_buy[1]
    else:
        amount = offer_to_sell[1]
    buy_fee = get_fee(the_cheapest_offer_to_buy[0])
    sell_fee = get_fee(offer_to_sell[0])
    profit = (amount * offer_to_sell[2] * (1 - buy_fee)) - \
                        (amount * the_cheapest_offer_to_buy[2] * (1 + sell_fee))
    return profit, amount


def check_markets():
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    print(f"Data obliczeń: {current_time}")
    for pair in currency_pairs:
        arbitration_table = get_arbitration_table(pair[0], pair[1], api_names)
        if not arbitration_table:
            print(f"\t Dla waluty {pair[0]} oraz {pair[1]} nie ma możliwości arbitrażu.")
        else:
            for arbitration in arbitration_table:
                print(f"\t Na giełdzie {arbitration[0]} można kupić {arbitration[1]} {pair[0]} za "
                      f"{pair[1]} po kursie {arbitration[2]:>.8f} i sprzedać na giełdzie {arbitration[3]} "
                      f" po kursie {arbitration[5]:>.8f}, zyskując {arbitration[6]:>.8f}{pair[1]}.")
                update_wallet(pair[1], arbitration[6])


def loop():
    while True:
        check_markets()
        print_wallet_info()
        sleep(refresh_period)
        print()


if __name__ == "__main__":
    loop()