# https://docs.bitfinex.com/reference
import time
import requests
import json

markets = [
    'tBTCUSD',
    'tLTCBTC',
    'tIOTBTC',
    'tDSHBTC',
]

def calculate_dif(ask, bid):
    dif = 1 - (ask - bid) / bid
    return dif

def get_data(market):
    response = requests.get(f'https://api-pub.bitfinex.com/v2/book/{market}/P0?len=1')
    dic = response.json()
    return (dic[1][0], dic[0][0])

def analyze_markets():
    while True:
        for market in markets:
            ask, bid = get_data(market)
            dif = calculate_dif(ask, bid)
            print("{}: Ask: {} | Bid: {} | Dif: {:.5f}%".format(market, ask, bid, dif*100))
        print()
        time.sleep(5)

analyze_markets()
