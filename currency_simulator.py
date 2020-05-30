from datetime import timezone, datetime
import requests
import matplotlib.pyplot as plt
import numpy as np



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
    bitstamp_json = bitstamp.json()
    return bitstamp_json


def analyze_data(currency_pair, start, end, step):
    data = gather_data(currency_pair, start, end, step)
    # print(data)
    make_plot(data['data']['ohlc'])
    simulate(data)


def simulate(data):
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
        close_percentage_change = close_diff / prev_close*100
        volume_percentage_change = volume_diff / prev_volume*100
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
    make_prediction(differences, 5, 4)


def make_prediction(data, last_timestamps, next_timestamps):
    # for i in range(next_timestamps)
    print("----------------")
    data = data[-last_timestamps::]
    print(data)
    close = [single_data['close'] for single_data in data]
    print(np.mean(close))
    print(np.median(close))
    print(np.std(close))


def make_plot(data):
    closing_prices = [float(period['close']) for period in data]
    volumes = [float(period['volume']) for period in data]
    timestamps = [float(period['timestamp']) for period in data]
    date_labels = map(convert_utc_to_date, timestamps)
    date_labels = list(date_labels)
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('date')
    ax1.set_ylabel('volume', color=color)
    ax1.set_ylim([0, 3 * max(volumes)])
    ax1.bar(date_labels, volumes, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel('closing price', color=color)
    ax2.plot(date_labels, closing_prices, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.gcf().autofmt_xdate()
    plt.show()


def main():
    analyze_data("btcusd", convert_date_to_utc(2020,3,15), convert_date_to_utc(2020,5,29), 3600 * 24)


if __name__ == "__main__":
    main()
