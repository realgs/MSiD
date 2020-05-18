import numpy

from time import sleep

import app.data as data
import app.logger as logger
import app.config as c

def analise_past_data():
    d = {}
    for market in c.MARKETS:
        market_data = data.get_tickers(market)
        buy_data = [x[0] for x in market_data]
        sell_data = [x[1] for x in market_data]
        avg_buy = numpy.mean(buy_data)
        avg_sell = numpy.mean(sell_data)
        min_buy = numpy.min(buy_data)
        max_buy = numpy.max(buy_data)
        min_sell = numpy.min(sell_data)
        max_sell = numpy.max(sell_data)
        d[market] = {
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
    return d

def evaluate(da):
    wallet = {k: v for (k, v) in data.get_wallet()}
    for market in c.MARKETS:
        d = da[market]
        last_ticker = data.get_last_ticker(market)
        (buy, sell) = last_ticker[0], last_ticker[1]
        currency = c.MARKET_CURRENCY_MAPPING[market]

        if d['BUY']['AVG'] < buy and d['SELL']['MIN'] < buy:
            if wallet[currency] > 0:
                # consider selling
                diff = buy - d['BUY']['AVG']
                trade_value = diff / (d['BUY']['MAX'] - d['BUY']['AVG'])
                trade_value = numpy.clip(trade_value, 0, 1)
                if trade_value > c.TRADE_VALUE_TRIGGER:
                    currency_to_trade = wallet[currency] * trade_value
                    gain = buy * currency_to_trade
                    data.update_in_wallet(currency, wallet[currency] - currency_to_trade)
                    data.update_in_wallet('USD', wallet['USD'] + gain)
                    logger.log(f'Sold {currency_to_trade} {currency}')
                    logger.log(f'Gained {gain} $')
                    logger.log(f'Current {currency}: {round(wallet[currency], 2)}')
                    logger.log(f'Current balance: {round(wallet["USD"], 2)} $')
                    logger.log()

        if d['SELL']['AVG'] > sell and d['BUY']['MAX'] < sell:
            if wallet['USD'] > 0:
                # consider buying
                diff = d['SELL']['AVG'] - sell
                trade_value = diff / (d['SELL']['AVG'] - d['SELL']['MIN'])
                trade_value = numpy.clip(trade_value, 0, 1)
                balance_to_trade = wallet['USD'] * trade_value
                if trade_value > c.TRADE_VALUE_TRIGGER:
                    currency_bought = balance_to_trade / sell
                    data.update_in_wallet('USD', wallet['USD'] - balance_to_trade)
                    data.update_in_wallet(currency, wallet[currency] + currency_bought)
                    logger.log(f'Bought {currency_bought} {currency}')
                    logger.log(f'Used {balance_to_trade} $')
                    logger.log(f'Current {currency}: {round(wallet[currency], 2)}')
                    logger.log(f'Current balance: {round(wallet["USD"], 2)} $')
                    logger.log()

def simulate():
    data_refresh_counter = 0
    logger.log('Starting simulation')
    d = analise_past_data()
    while True:
        evaluate(d)
        data_refresh_counter += 1
        if data_refresh_counter % c.REFRESH_DATA_EVERY == 0:
            d = analise_past_data()
        sleep(c.REFRESH_DATA_EVERY)
