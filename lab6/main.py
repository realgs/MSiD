import requests
import datetime
from statistics import mean, stdev, median
import matplotlib.pyplot as plt
from currencyData import generate_url, prepare_values, generate_dates, generate_future_values, generate_stats
from forecaster import Generator


def print_price_chart(first_series, second_series):
    x, y, bars = first_series
    plt.xlabel('date')
    plt.ylabel('price[USD], volume[10^7]')
    plt.xticks(rotation=60)
    plt.plot(x, y)
    plt.bar(x, bars, color=['green', 'blue'])
    x, y, bars = second_series
    plt.plot(x, y)
    plt.bar(x, bars, color=['red', 'orange'])
    plt.show()


def print_bar_char(data, time, title):
    plt.xticks(rotation=60)
    plt.title(title)
    plt.bar(time, data)
    plt.show()


if __name__ == '__main__':
    url = generate_url('2018-03-29', '2018-04-29', interval='3h')
    data = requests.get(url).json()
    dates, prices, volumes = prepare_values(data)
    model = Generator(prices, volumes)
    future_prices, future_volumes = generate_future_values(model)
    future_dates = generate_dates('2018-04-29 00:00:00', datetime.timedelta(hours=3), len(dates))
    average_prices, average_volumes = generate_stats(future_prices, future_volumes, mean)
    print_price_chart((dates, prices, volumes), (future_dates, average_prices, average_volumes))
    price_dev, volume_dev = generate_stats(future_prices, future_volumes, stdev)
    price_median, volume_median = generate_stats(future_prices, future_volumes, median)
    print_bar_char(price_dev, future_dates, 'price deviations')
    print_bar_char(volume_dev, future_dates, 'volumes deviations')
    print_bar_char(price_median, future_dates, 'price medians')
    print_bar_char(volume_median, future_dates, 'volume medians')

