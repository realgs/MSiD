from app.config import BITBAY_API_URL, TRADING_FEE
from app.utils import get_json_data

def extract_buy_sell(data):
    buy = float(data['ticker']['highestBid']) * (1 - TRADING_FEE)
    sell = float(data['ticker']['lowestAsk']) * (1 + TRADING_FEE)
    return (buy, sell)

def get_buy_sell(market):
    url = f"{BITBAY_API_URL}{market}"
    data = get_json_data(url)
    return extract_buy_sell(data)


