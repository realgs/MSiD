#!/usr/bin/env python3

import urllib.request, json
from time import sleep
import sqlite3
import numpy

conn = sqlite3.connect("database.db")
c = conn.cursor()

TRADE_VALUE_TRIGGER = 0.2 # how good a trade has to be to make a transaction
REFRESH_DATA_EVERY = 50 # how often to refresh data

balance = 3000

currencies = [
    'BTC',
    'LTC',
    'ETH',
    'XRP',
]

wallet = {
    'BTC': 0,
    'LTC': 0,
    'ETH': 0,
    'XRP': 0,
}

fee = 0.0010

markets = [
    'BTC-USD',
    'LTC-USD',
    'ETH-USD',
    'XRP-USD',
]

market_currency_mapping = {
    'BTC-USD': 'BTC',
    'LTC-USD': 'LTC',
    'ETH-USD': 'ETH',
    'XRP-USD': 'XRP',
}

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

def analise_past_data():
    print('Gathering data...')
    data = {}
    for market in markets:
        market_data = c.execute('SELECT buy, sell FROM data WHERE market = ?', (market,)).fetchall()
        buy_data = [x[0] for x in market_data]
        sell_data = [x[1] for x in market_data]
        avg_buy = numpy.mean(buy_data)
        avg_sell = numpy.mean(sell_data)
        min_buy = numpy.min(buy_data)
        max_buy = numpy.max(buy_data)
        min_sell = numpy.min(sell_data)
        max_sell = numpy.max(sell_data)
        data[market] = {
            'BUY': {
                'AVG': avg_buy,
                'MIN': min_buy,
                'MAX': max_buy,
            },
            'SELL': {
                'AVG': avg_sell,
                'MIN': min_sell,
                'MAX': max_sell,
            },
        }
    return data

def evaluate(data):
    global wallet, balance
    for market in markets:
        d = data[market]
        (buy, sell) = get_buy_sell(market)
        c.execute("INSERT INTO data (buy, sell, market) VALUES (?, ?, ?)", (buy, sell, market))
        conn.commit()
        currency = market_currency_mapping[market]

        if d['BUY']['AVG'] < buy and d['SELL']['MIN'] < buy:
            if wallet[currency] > 0:
                # consider selling
                diff = buy - d['BUY']['AVG']
                trade_value = diff / (d['BUY']['MAX'] - d['BUY']['AVG'])
                trade_value = numpy.clip(trade_value, 0, 1)
                if trade_value > TRADE_VALUE_TRIGGER:
                    currency_to_trade = wallet[currency] * trade_value
                    gain = buy * currency_to_trade
                    wallet[currency] -= currency_to_trade
                    balance += gain
                    print(f'Sold {currency_to_trade} {currency}')
                    print(f'Gained {gain} $')
                    print(f'Current {currency}: {round(wallet[currency], 2)}')
                    print(f'Current balance: {round(balance, 2)} $')
                    print()

        if d['SELL']['AVG'] > sell and d['BUY']['MAX'] < sell:
            if balance > 0:
                # consider buying
                diff = d['SELL']['AVG'] - sell
                trade_value = diff / (d['SELL']['AVG'] - d['SELL']['MIN'])
                trade_value = numpy.clip(trade_value, 0, 1)
                balance_to_trade = balance * trade_value
                if trade_value > TRADE_VALUE_TRIGGER:
                    currency_bought = balance_to_trade / sell
                    balance -= balance_to_trade
                    wallet[currency] += currency_bought
                    print(f'Bought {currency_bought} {currency}')
                    print(f'Used {balance_to_trade} $')
                    print(f'Current {currency}: {round(wallet[currency], 2)}')
                    print(f'Current balance: {round(balance, 2)} $')
                    print()

def simulate():
    data_refresh_counter = 0
    print('Starting simulation')
    data = analise_past_data()
    while True:
        evaluate(data)
        data_refresh_counter += 1
        if data_refresh_counter % REFRESH_DATA_EVERY == 0:
            data = analise_past_data()
        sleep(5)

if __name__ == "__main__":
    simulate()
