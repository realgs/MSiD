import apiBroker
import time
import datetime
import numpy as np
import pandas as pd

pairs = [
    "BTC-USD",
    "ETH-USD",
    "LTC-USD"
]


# YYYY-MM_DD format
def convert_dates(human_readable_date):
    (yyyy, mm, dd) = (human_readable_date.split("-"))
    date = datetime.datetime(int(yyyy), int(mm), int(dd))
    return int(date.timestamp())


def sim(trading_pair, starting_date, ending_date):
    starting_date = convert_dates(starting_date)
    ending_date = convert_dates(ending_date)
    if ending_date >= time.time() or starting_date >= ending_date:
        raise ValueError("Wrong date range")
    if trading_pair not in pairs:
        raise ValueError("Wrong trading pair")
    data = pd.DataFrame(apiBroker.get_data(trading_pair, starting_date, ending_date))
    count_rise_probability(data)


def count_rise_probability(data):
    data['diff'] = data['open'] - data['close']
    total_change_in_price = np.abs(data['diff']).sum()
    print((data['diff'][data['diff'] > 0]).sum())
    print(total_change_in_price)
    print((data['diff'][data['diff']]).sum() / total_change_in_price)


if __name__ == '__main__':
    sim("BTC-USD", "2020-04-18", "2020-05-24")
