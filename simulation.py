from datetime import datetime, timedelta
from api import get_need_data
import time

import math
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

import plotly.graph_objects as go
from plotly.subplots import make_subplots

START_TIME = datetime(2020, 1, 1)
END_TIME = datetime(2020, 5, 31)

pairs = ['BTC USD', 'ETH USD', 'LTC USD']


def get_data(time_from, time_to, pair):
    data = get_need_data(time_from, time_to, pair)

    for sth in data:
        sth['diff'] = (sth['open'] - sth['close']) / sth['open'] * 100

    data_frame = pd.DataFrame(data)
    data_frame = data_frame.drop(columns=['quoteVolume', 'weightedAverage'])

    return data_frame


def simulation(days, time_from, time_to, pair, iterations):
    df = get_data_frame(time_from, time_to, pair)
    df2 = get_data_frame(time_from, time_to, pair)
    dataset2 = df2.values
    data = df.filter(['high', 'low', 'open', 'close', 'volume'])
    dataset = data.values

    day = END_TIME

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    train_data = scaled_data.copy()
    x_train = []
    y_train = []

    if len(train_data) >= 100:
        for i in range(60, len(train_data)):
            x_train.append(train_data[i - 60:i, :])
            y_train.append(train_data[i, :])
    else:
        helper = math.ceil((len(train_data) / 60) * 10)
        for i in range(helper, len(train_data)):
            x_train.append(train_data[i - helper:i, :])
            y_train.append(train_data[i, :])

    x_train, y_train = np.array(x_train), np.array(y_train)

    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(5))

    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x_train, y_train, batch_size=1, epochs=1)

    last_days = df[-60:].filter(['high', 'low', 'open', 'close', 'volume'])
    last_days = last_days.values
    last_days_scaled = scaler.transform(last_days)
    x_test = []
    x_test.append(last_days_scaled)
    x_test = np.array(x_test)
    result = []

    for i in range(days):
        price = model.predict(x_test, use_multiprocessing=True)
        price = list(price)
        arr = []

        for j in range(len(x_test[0])):
            sth = x_test[0][j]
            sth = list(sth)
            arr.append(sth)

        arr.append(price[0])
        result.append(price[0])
        arr = list(arr)
        del arr[0]

        arr = np.array(arr)
        arr = np.reshape(arr, (1, arr.shape[0], arr.shape[1]))

        x_test = arr

    result = scaler.inverse_transform(result)

    dataset2 = list(dataset2)

    for i in range(len(result)):
        sth = []
        sth.append(datetime.timestamp(day))
        for j in range(len(result[0])):
            sth.append(result[i][j])
        sth.append(((result[i][2] - result[i][3]) / result[i][2] * 100))
        sth = np.array(sth)
        dataset2.append(sth)
        day += timedelta(days=1)

    new_df = pd.DataFrame(dataset2, columns=['time', 'high', 'low', 'open', 'close', 'volume', 'diff'])

    plot(new_df, pair)


def plot(df, pair):
    df['time'] = df['time'].apply(lambda x: datetime.fromtimestamp(x))
    print(df)

    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=('Stock prices', 'Percentage change', 'Volume'))
    fig.add_trace(
        go.Candlestick(
            name='Stock prices',
            x=df['time'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
        ),
        row=1, col=1,
    )
    fig.add_trace(
        go.Bar(
            name='Percentage change',
            x=df['time'],
            y=df['diff'],
        ),
        row=1, col=2,
    )
    fig.add_trace(
        go.Bar(
            name='Volume',
            x=df['time'],
            y=df['volume'],
        ),
        row=2, col=1,
    )

    line_date = END_TIME - timedelta(hours=12)
    fig.update_layout(title_text=f'{pairs[pair-1]} predictions',
                      shapes=[dict(
                          x0=line_date, x1=line_date, y0=0, y1=1, xref='x', yref='paper', line_width=2,
                      )])

    fig.show()


def get_data_frame(time_from, time_to, pair):
    if time_from >= time.time() or time_from >= time_to:
        raise ValueError("Wrong date range")

    data_frame = get_data(time_from, time_to, pair)
    return data_frame


if __name__ == '__main__':
    simulation(20, datetime.timestamp(START_TIME), datetime.timestamp(END_TIME), 1, 100)
