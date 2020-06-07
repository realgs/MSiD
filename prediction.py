import json
import requests
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
import plotly.graph_objects as graph_obj
from plotly.subplots import make_subplots
from sklearn import linear_model
from sklearn.model_selection import train_test_split

CURRENCY_PAIRS = ['BTC_ETH', 'BTC_LTC']
PERIOD = 7200


def get_url_data(url):
    try:
        request = requests.get(url)
        data = json.loads(request.text)
        return data
    except requests.exceptions.ConnectionError:
        print("No connection")
        return None


def create_chart_history_url(currency_pair, begin_date, end_date, period):
    return f"https://poloniex.com/public?command=returnChartData&currencyPair={currency_pair}&" \
           f"start={convert_date_to_seconds(begin_date)}&end={convert_date_to_seconds(end_date)}&period={period}"


def convert_date_to_seconds(date):
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    hour = int(date[11:13])
    minute = int(date[14:16])
    second = int(date[17:19])
    return datetime.timestamp(datetime(year, month, day, hour, minute, second))


def speculate_price(currency_pair, begin_date, end_date, days_to_predict):
    chart_history_data = get_url_data(create_chart_history_url(currency_pair, begin_date, end_date, PERIOD))
    chart_dict = {'open': [], 'high': [], 'low': [], 'close': [], 'price': [], 'volume': [], 'time': []}

    for data in chart_history_data:
        chart_dict['time'].append(data['date'])
        chart_dict['price'].append(data['weightedAverage'])
        chart_dict['open'].append(data['open'])
        chart_dict['high'].append(data['high'])
        chart_dict['low'].append(data['low'])
        chart_dict['close'].append(data['close'])
        chart_dict['volume'].append(data['quoteVolume'])

    df_x = pd.DataFrame(chart_dict['time'])
    # predicting close prices
    df_y = pd.DataFrame(chart_dict['close'])

    reg = linear_model.LinearRegression()
    x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.5, random_state=3)

    reg.fit(x_train, y_train)
    periods = []
    candle_time = time.time()
    for i in range(0, int((24/(PERIOD/3600))*days_to_predict)):
        periods.append(candle_time)
        candle_time += PERIOD

    x_future_time = pd.DataFrame(periods)

    a = reg.predict(x_future_time)

    min_range = len(chart_dict['price'])
    max_range = len(chart_dict['price']) + len(x_future_time)

    for i in range(min_range, max_range):
        chart_dict['time'].append(x_future_time)
        chart_dict['price'].append(a[i - min_range])
        chart_dict['open'].append(a[i - min_range])
        chart_dict['high'].append(a[i - min_range])
        chart_dict['low'].append(a[i - min_range])
        chart_dict['close'].append(a[i - min_range])
        chart_dict['volume'].append(0)

    return chart_dict


def create_plot(currency_pair, chart_data):
    plot = make_subplots(rows=2, cols=1, subplot_titles=(f'{currency_pair} stock price', '', ''))
    plot.add_trace(graph_obj.Candlestick(name='Price', open=chart_data['open'], high=chart_data['high'],
                                         low=chart_data['low'], close=chart_data['close'], x=chart_data['time']),
                   row=1, col=1)
    plot.add_trace(graph_obj.Bar(name=f'Volume for {currency_pair}',
                                 x=chart_data['time'], y=chart_data['volume']), row=2, col=1)
    plot.show()


def main():
    create_plot(CURRENCY_PAIRS[0], speculate_price(CURRENCY_PAIRS[0], '2020.06.05@20:52:30', '2020.06.06@20:52:30', 5))


if __name__ == "__main__":
    main()
