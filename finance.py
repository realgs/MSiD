#!/usr/bin/env python3

import urllib.request, json
from time import sleep

markets=[
    'BTC-LTC',
    'BTC-DOGE',
    'BTC-PPC',
    'BTC-FTC',
    'BTC-RDD',
]

def get_json_data(url):
    with urllib.request.urlopen(url) as u:
        return json.loads(u.read().decode())

def get_buy_sell(market):
    url = f"https://api.bittrex.com/api/v1.1/public/getticker?market={market}"
    data = get_json_data(url)
    return (data['result']['Bid'], data['result']['Ask'])

def print_buy_sell():
    for market in markets:
        (buy, sell) = get_buy_sell(market)
        print(f'{market}: Buy for {buy}, Sell for {sell}')

def get_percent_diff(buy, sell):
    return 1 - (sell - buy) / buy

def print_buy_sell_percent_diff():
    data = {market:get_percent_diff(*get_buy_sell(market)) for market in markets}
    print('\n'.join([f'{market}: {percent}' for (market, percent) in data.items()]))

def monitor_buy_sell_percent_diff():
    while True:
        print_buy_sell_percent_diff()
        sleep(5)

# print_buy_sell()
monitor_buy_sell_percent_diff()
