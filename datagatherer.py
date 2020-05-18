import sqlite3
import time
from datetime import datetime
import Stocks

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

trading_pairs = [
    "BTC-USD",
    "LTC-USD",
    "ETH-USD",
    "XRP-USD"
]

def gather_data():
    for pair_index in range(4):
        (bid, ask) = Stocks.get_sells_and_buys('bitbay', pair_index)
        val = (bid + ask) / 2
        cursor.execute("INSERT INTO data VALUES (?,?,?)",
                       (datetime.now().strftime("%m/%d/%Y %H:%M:%S"), val, trading_pairs[pair_index]))
        connection.commit()

def gather_data_loop():
    while True:
        for pair_index in range(4):
            (bid, ask) = Stocks.get_sells_and_buys('bitbay', pair_index)
            val = (bid + ask) / 2
            cursor.execute("INSERT INTO data VALUES (?,?,?)", (datetime.now().strftime("%m/%d/%Y %H:%M:%S"), val, trading_pairs[pair_index]))
            connection.commit()
        time.sleep(60)


if __name__ == '__main__':
    gather_data_loop()
