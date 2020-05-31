from datetime import timezone, datetime
import requests
import matplotlib.pyplot as plt
import numpy as np
import random

supported_steps = [60, 180, 300, 900, 1800, 3600, 7200, 14400, 21600, 43200, 86400, 259200]
supported_pairs = ["btcusd", "btceur", "eurusd", "xrpusd", "xrpeur", "xrpbtc", "ltcusd", "ltceur", "ltcbtc", "ethusd",
                   "etheur", "ethbtc", "bchusd", "bcheur", "bchbtc"]


def convert_date_to_utc(year, month, day, hour=0, minutes=0, seconds=0):
    dt = datetime(year, month, day, hour, minutes, seconds)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    return int(timestamp)


def convert_utc_to_date(timestamp):
    return datetime.fromtimestamp(timestamp)


def gather_data(currency_pair, start, end, step):
    limit = (end - start) // step + 1
    bitstamp = requests.get("https://www.bitstamp.net/api/v2/ohlc/{0}/".format(currency_pair),
                            params={'start': start, 'end': end, 'step': step, 'limit': limit})
    if bitstamp.status_code == 200:
        bitstamp_json = bitstamp.json()
        return True, bitstamp_json
    else:
        return False, None


def analyze_data(currency_pair, start, end, last_timestamps, next_timestamps, iterations, step):
    valid, data = gather_data(currency_pair, start, end, step)
    if valid:
        simulated_data = simulate(data, last_timestamps, next_timestamps, iterations, step)
        make_plot(simulated_data, data['data']['pair'], end)
    else:
        print("ERROR GATHERING DATA")


def prepare_single_data(timestamp, close, volume, prev_close, prev_volume):
    close_diff = close - prev_close
    volume_diff = volume - prev_volume
    close_percentage_change = close_diff / prev_close * 100
    volume_percentage_change = volume_diff / prev_volume * 100
    return {
        'timestamp': timestamp,
        'close': close,
        'volume': volume,
        'close_diff': close_diff,
        'volume_diff': volume_diff,
        'close_percentage_change': close_percentage_change,
        'volume_percentage_change': volume_percentage_change
    }


def simulate(data, last_timestamps, next_timestamps, iterations, step):
    differences = []
    data = data['data']['ohlc']
    previous_data = data[0]
    for period in data[1::]:
        differences.append(
            prepare_single_data(int(period['timestamp']), float(period['close']), float(period['volume']),
                                float(previous_data['close']), float(previous_data['volume'])))
        previous_data = period
    make_predictions(differences, last_timestamps, next_timestamps, iterations, step)
    return differences


def make_predictions(data, last_timestamps, next_timestamps, iterations, step):
    for i in range(next_timestamps):
        data_segment = data[-last_timestamps::]
        close = [single_data['close'] for single_data in data_segment]
        close_diff = [single_data['close_diff'] for single_data in data_segment]
        close_percentage_change = [single_data['close_percentage_change'] for single_data in data_segment]
        close_positive_count = sum(x > 0 for x in close_percentage_change)
        close_grow_chance = close_positive_count / last_timestamps

        volume = [single_data['volume'] for single_data in data_segment]
        volume_diff = [single_data['volume_diff'] for single_data in data_segment]
        volume_percentage_change = [single_data['volume_percentage_change'] for single_data in data_segment]

        volume_positive_count = sum(x > 0 for x in volume_percentage_change)
        volume_grow_chance = volume_positive_count / last_timestamps

        close_values = []
        volume_values = []
        for j in range(iterations):
            close_is_growing = random.random() <= close_grow_chance
            close_percentage_change = np.mean(np.abs(close_percentage_change)) * random.uniform(0.5, 1.5) * (1 if close_is_growing else -1)
            new_close = round(close[-1] *(1+close_percentage_change/100), 2)
            close_values.append(new_close)

            volume_is_growing=True
            if close_percentage_change<-5 or close_percentage_change>5:
                volume_is_growing = True
            else:
                volume_is_growing = random.random() <= volume_grow_chance
            volume_percentage_change = np.mean(np.abs(volume_percentage_change)) * random.uniform(0.2, 1.6) * (1 if volume_is_growing else -1)
            new_volume = round(volume[-1]*(1+volume_percentage_change/100), 2)
            volume_values.append(new_volume)

        print("timestamp: {0}".format(data_segment[-1]['timestamp']+ step))
        print("close - MEAN: {0}, MEDIAN: {1}, STANDARD DEVIATION: {2}".format(np.mean(close_values),np.median(close_values),np.std(close_values)))
        print("volume - MEAN: {0}, MEDIAN: {1}, STANDARD DEVIATION: {2}".format(np.mean(volume_values),np.median(volume_values),np.std(volume_values)))
        new_close = np.mean(close_values)
        new_volume = np.mean(volume_values)
        data.append(prepare_single_data(data_segment[-1]['timestamp'] + step, new_close, new_volume,
                                        data_segment[-1]['close'], data_segment[-1]['volume']))


def make_plot(data, currency_pair, end_date):
    closing_prices = [period['close'] for period in data]
    volumes = [period['volume'] for period in data]
    timestamps = [period['timestamp'] for period in data]

    date_labels = map(convert_utc_to_date, timestamps)
    date_labels = list(date_labels)

    plt.style.use('bmh')
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
    ax2.plot(date_labels, closing_prices, color=color, alpha=0.75)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title(currency_pair)
    plt.axvline(x=convert_utc_to_date(end_date), color='tab:green', alpha=0.5)
    plt.gcf().autofmt_xdate()

    plt.show()


def main():
    analyze_data(currency_pair="btcusd", start=convert_date_to_utc(2020, 3, 1), end=convert_date_to_utc(2020, 5, 29),
                 last_timestamps=50, next_timestamps=20, iterations=20, step=3600*24)


if __name__ == "__main__":
    main()
