#!/usr/bin/env python3

import urllib.request, json
from time import sleep
import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

fee = 0.0010

markets = [
    'BTC-USD',
    'LTC-USD',
    'ETH-USD',
    'XRP-USD',
]

bitbay_url = 'https://api.bitbay.net/rest/trading/ticker/'

def get_json_data(url):
    with urllib.request.urlopen(url) as u:
        return json.loads(u.read().decode())

def extract_buy_sell(data):
    return (float(data['ticker']['highestBid']) * (1 - fee), float(data['ticker']['lowestAsk']) * (1 + fee))

def get_buy_sell(market):
    url = f"{bitbay_url}{market}"
    data = get_json_data(url)
    return extract_buy_sell(data)

def gather_data_once():
    for market in markets:
        (buy, sell) = get_buy_sell(market)
        print((buy, sell, market))
        c.execute("INSERT INTO data (buy, sell, market) VALUES (?, ?, ?)", (buy, sell, market))
    conn.commit()

def gather_data():
    while True:
        gather_data_once()
        sleep(5)

if __name__ == "__main__":
    gather_data()
