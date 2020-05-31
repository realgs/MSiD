from datetime import timezone, datetime
import requests
import matplotlib.pyplot as plt
import numpy as np
import random

step = 300


def convert_date_to_utc(year, month, day, hour=0, minutes=0, seconds=0):
    dt = datetime(year, month, day, hour, minutes, seconds)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    return int(timestamp)


def convert_utc_to_date(timestamp):
    return datetime.fromtimestamp(timestamp)


def gather_data(currency_pair, start, end):
    limit = (end - start) // step + 1
    bitstamp = requests.get("https://www.bitstamp.net/api/v2/ohlc/{0}/".format(currency_pair),
                            params={'start': start, 'end': end, 'step': step, 'limit': limit})
    bitstamp_json = bitstamp.json()
    return bitstamp_json


def analyze_data(currency_pair, start, end, last_timestamps, next_timestamps):
    data = gather_data(currency_pair, start, end)
    # print(data)
    simulated_data = simulate(data, last_timestamps, next_timestamps)
    make_plot(simulated_data, end)


def simulate(data, last_timestamps, next_timestamps):
    differences = []
    data = data['data']['ohlc']
    print(data)
    previous_data = data[0]
    print(previous_data)
    for period in data[1::]:
        curr_timestamp = int(period['timestamp'])
        prev_close = float(previous_data['close'])
        prev_volume = float(previous_data['volume'])
        curr_close = float(period['close'])
        curr_volume = float(period['volume'])
        close_diff = curr_close - prev_close
        volume_diff = curr_volume - prev_volume
        close_percentage_change = close_diff / prev_close * 100
        volume_percentage_change = volume_diff / prev_volume * 100
        differences.append({
            'timestamp': curr_timestamp,
            'close': curr_close,
            'volume': curr_volume,
            'close_diff': close_diff,
            'volume_diff': volume_diff,
            'close_percentage_change': close_percentage_change,
            'volume_percentage_change': volume_percentage_change
        })
        print("CLOSING PRICE: {0}".format(curr_close))
        print("VOLUME: {0}".format(curr_volume))
        print("CLOSING PRICE DIFF: {0}".format(curr_close - prev_close))
        print("VOLUME DIFF: {0}".format(curr_volume - prev_volume))
        print(period)
        previous_data = period
    for difference in differences:
        print(difference)
    make_prediction(differences, last_timestamps, next_timestamps)
    print("----------------")
    for period in differences[-next_timestamps::]:
        print(period)
    return differences



def make_prediction(data, last_timestamps, next_timestamps):
    for i in range(next_timestamps):
        # print("----------------")
        iteration_data = data[-last_timestamps::]
        close = [single_data['close'] for single_data in iteration_data]
        close_diff = [single_data['close_diff'] for single_data in iteration_data]
        close_percentage_change = [single_data['close_percentage_change'] for single_data in iteration_data]
        # print(np.mean(close))
        # print(np.median(close))
        # print(np.std(close))

        close_positive_count = sum(x > 0 for x in close_percentage_change)
        close_grow_chance = close_positive_count / last_timestamps
        close_is_growing = random.random() <= close_grow_chance
        close_change = abs(np.mean(close_diff)) * random.uniform(0.1, 10) * (1 if close_is_growing else -1)
        # print(np.mean(close_diff))
        new_close = round(close[-1] + close_change, 2)
        # print(new_close)

        volume = [single_data['volume'] for single_data in iteration_data]
        volume_diff = [single_data['volume_diff'] for single_data in iteration_data]
        volume_percentage_change = [single_data['volume_percentage_change'] for single_data in iteration_data]
        volume_positive_count = sum(x > 0 for x in volume_percentage_change)
        volume_grow_chance = volume_positive_count / last_timestamps
        volume_is_growing = random.random() <= volume_grow_chance
        volume_change = abs(np.mean(volume_diff)) * random.uniform(0.5, 1.5) * (1 if volume_is_growing else -1)
        # print(np.mean(volume_percentage_change))
        # print(volume_diff)
        new_volume = round(volume[-1] + volume_change, 2)
        # print(new_volume)
        close_diff = new_close - iteration_data[-1]['close']
        volume_diff = new_volume - iteration_data[-1]['volume']
        close_percentage_change = close_diff / iteration_data[-1]['close'] * 100
        volume_percentage_change = volume_diff / iteration_data[-1]['close'] * 100
        data.append({
            'timestamp': iteration_data[-1]['timestamp'] + step,
            'close': new_close,
            'volume': new_volume,
            'close_diff': close_diff,
            'volume_diff': volume_diff,
            'close_percentage_change': close_percentage_change,
            'volume_percentage_change': volume_percentage_change
        })
        # print(data[-1])


def make_plot(data, end_date):
    print(data)
    closing_prices = [period['close'] for period in data]
    volumes = [period['volume'] for period in data]
    timestamps = [period['timestamp'] for period in data]
    date_labels = map(convert_utc_to_date, timestamps)
    date_labels = list(date_labels)
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('date')
    ax1.set_ylabel('volume', color=color)
    ax1.set_ylim([0, 3 * max(volumes)])
    ax1.bar(date_labels, volumes, color=color, alpha=0.75)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel('closing price', color=color)
    ax2.plot(date_labels, closing_prices, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.axvline(x=convert_utc_to_date(end_date), color='tab:green', alpha=0.5)
    plt.gcf().autofmt_xdate()

    plt.show()


def main():
    global step
    step = 3600 * 24
    analyze_data("btcusd", convert_date_to_utc(2020, 3, 15), convert_date_to_utc(2020, 5, 29), 100, 10)


if __name__ == "__main__":
    main()
