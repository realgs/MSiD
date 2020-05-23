import apiBroker
import time

pairs = [
    "BTC-USD",
    "ETH-USD",
    "LTC-USD"
]


def sim(trading_pair, starting_date, ending_date):
    if ending_date >= time.time() or starting_date >= ending_date:
        raise ValueError("Wrong date range")
    if trading_pair not in pairs:
        raise ValueError("Wrong trading pair")
    data = apiBroker.get_all_data(trading_pair)

def check_if_price_has_risen(open, close):
    return close > open

def count_probabilities(data):
    a = 0
    total_volume = 0
    for record in data["Data"]:
        pass#???


if __name__ == '__main__':
    sim("BTC-USD", 1589328000, 1590192000)