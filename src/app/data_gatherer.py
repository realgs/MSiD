from time import sleep

import app.data as data
import app.logger as logger

from app.bitbay import get_buy_sell
from app.config import MARKETS, REFRESH_EVERY

def gather_data_once():
    for market in MARKETS:
        (buy, sell) = get_buy_sell(market)
        # logger.log((buy, sell, market))
        data.insert_market_data(buy, sell, market)

def gather_data():
    while True:
        gather_data_once()
        sleep(REFRESH_EVERY)
