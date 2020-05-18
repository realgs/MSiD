WALLET_TABLE = 'Wallet'
TICKER_TABLE = 'Tickers'

import sqlite3
import threading

lock = threading.Lock()

conn = sqlite3.connect('app/database/database.db', check_same_thread=False)
c = conn.cursor()

def fetchall(sql, *args):
    with lock:
        return c.execute(sql, *args).fetchall()

def get_wallet():
    return fetchall(f'SELECT Currency, Value FROM {WALLET_TABLE}')

def insert_into_wallet(currency_value_map):
    with lock:
        for currency, value in currency_value_map.items():
            c.execute(f'INSERT INTO {WALLET_TABLE} (Currency, Value) VALUES (?, ?)', (currency, value))
        conn.commit()

def update_in_wallet(currency, value):
    with lock:
        c.execute(f'UPDATE {WALLET_TABLE} SET Value=(?) WHERE Currency=(?)', (value, currency))
        conn.commit()

def delete_wallet():
    with lock:
        c.execute(f'DELETE FROM {WALLET_TABLE}')
        conn.commit()

def insert_market_data(buy, sell, market):
    with lock:
        c.execute(f'INSERT INTO {TICKER_TABLE} (buy, sell, market) VALUES (?, ?, ?)', (buy, sell, market))
        conn.commit()

def get_tickers(market):
    return fetchall(f'SELECT buy, sell, date FROM {TICKER_TABLE} WHERE market=(?)', (market,))

def get_last_ticker(market):
    return fetchall(f'SELECT buy, sell, date FROM {TICKER_TABLE} WHERE market=(?) LIMIT 1', (market,))[0]
