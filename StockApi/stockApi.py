import requests
from time import sleep

markets = ["BTC-LTC", "BTC-DGB", "BTC-HIVE"]


def get_buy_sell_list(market):
    url = "https://api.bittrex.com/api/v1.1/public/getticker?market="+market
    resp = requests.get(url)
    data = resp.json()
    return data['result']['Bid'], data['result']['Ask']


def print_buy_sell_list():
    for market in markets:
        data = get_buy_sell_list(market)
        print(market, 'Buy', data[1], 'Sell', data[0])


def get_buy_sell_percent_diff(data):
    return 1-(data[1]-data[0])/data[0]


def print_buy_sell_percent():
    for market in markets:
        percent = get_buy_sell_percent_diff(get_buy_sell_list(market))
        print(market, percent)


def update_percent_list():
    while True:
        print_buy_sell_percent()
        sleep(5)


# print_buy_sell_list()
# print_buy_sell_percent()
update_percent_list()
