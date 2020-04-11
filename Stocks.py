import requests
from time import sleep


def get_markets():
    markets = []
    url = f"https://api.bitbay.net/rest/trading/ticker"
    headers = {'content-type': 'application/json'}

    data = requests.request("GET", url, headers=headers).json()
    for item in data['items']:
        markets.append(item)
    return markets


def get_data(market):
    url = f"https://api.bitbay.net/rest/trading/ticker/{market}"
    headers = {'content-type': 'application/json'}

    response = requests.request("GET", url, headers=headers)
    return response.json()


def get_sells_and_buys_market(market):
    data = get_data(market)
    return float(data['ticker']['highestBid']), float(data['ticker']['lowestAsk'])


def print_sells_and_buys_market(market):
    print(get_sells_and_buys_market(market))


def print_sells_and_buys_(markets):
    for market in markets:
        print("{0}: {1}".format(market, get_sells_and_buys_market(market)))


def calc_diff(bid, ask):
    return 1 - abs(bid - ask) / ask


def print_current_diff(market):
    while True:
        (bid, ask) = get_sells_and_buys_market(market)
        print(calc_diff(bid, ask))
        sleep(5)


print_current_diff('BTC-PLN')
