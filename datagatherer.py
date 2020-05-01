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
    while True:
        for pair_index in range(4):
            (bid, ask) = Stocks.get_sells_and_buys('bitbay', pair_index)
            val = (bid + ask) / 2
            cursor.execute("INSERT INTO data VALUES (?,?,?)", (datetime.now().strftime("%m/%d/%Y %H:%M:%S"), val, trading_pairs[pair_index]))
            connection.commit()
        time.sleep(60)


def print_db():

    cursor.execute('SELECT * FROM data')
    print(cursor.fetchall())

if __name__ == '__main__':
    gather_data()
