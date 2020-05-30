import apiBroker
import time
import datetime
import numpy as np
import pandas as pd
import graphs

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


def sim(trading_pair, starting_date, ending_date, count):
    data_list = []
    for i in range(count):
        data_list.append(sim_one(trading_pair, starting_date, ending_date))
    return data_list


def sim_one(trading_pair, starting_date, ending_date):
    starting_date = convert_dates(starting_date)
    ending_date = convert_dates(ending_date)
    if ending_date >= time.time() or starting_date >= ending_date:
        raise ValueError("Wrong date range")
    if trading_pair not in pairs:
        raise ValueError("Wrong trading pair")
    data = pd.DataFrame(apiBroker.get_data(trading_pair, starting_date, ending_date))
    data = data[['time', 'open', 'close', 'volumefrom']]
    days = int((ending_date - starting_date) / (24 * 60 * 60))
    data['months'] = int(days / 30)
    data['months'] = data['months'].clip(lower=1)
    for i in range(days):
        data = data.append(generate_entry(data), ignore_index=True)
    data = data.drop(columns=['months', 'diff'])
    return data


def generate_entry(data):
    price_change = (decide_how_price_changes(data, count_rise_probability(data)))
    new_volume = decide_volume_change(data, price_change)
    last_entry = data.tail(1)
    time = last_entry['time'] + (24 * 60 * 60)  # 24 hours in seconds
    open = last_entry['close']
    close = open + price_change
    diff = np.abs(price_change)
    new_entry = pd.DataFrame({'time': time, 'open': open, 'volumefrom': new_volume, 'close': close, 'diff': diff})
    return new_entry


def decide_volume_change(data, price_change):
    diff = np.abs(price_change)
    result_index = data['diff'].sub(diff).abs().idxmin()
    return data.iloc[result_index, :]['volumefrom']


def count_rise_probability(data):
    data['diff'] = data['open'] - data['close']
    total_change_in_price = np.abs(data['diff']).sum()
    return (data['diff'][data['diff'] > 0]).sum() / total_change_in_price


def decide_how_price_changes(data, probability_of_rise):
    diffs = data['diff'].abs()
    p = np.random.uniform(diffs.min(), diffs.max()) / data.iloc[0]['months']
    if np.random.rand() < probability_of_rise:
        return p
    else:
        a = data.tail(1).iloc[0]['close'] - p
        if a - p < 0:
            return np.abs(a)
        else:
            return -p


def count_statistics(data):
    return {'averages': data.mean(), 'median': data.median(), 'deviation': data.std()}


def mean_from_multiple_sims(data_list):
    combined = pd.concat(data_list)
    means = combined.groupby(combined.index).mean()
    return means


if __name__ == '__main__':
    #datao = sim_one("BTC-USD", "2020-01-01", "2020-05-01")
    data = sim("BTC-USD", "2020-01-01", "2020-05-01", 5)
    graphs.draw(mean_from_multiple_sims(data), 'Avg')
