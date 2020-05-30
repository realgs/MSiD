import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from app import cryptocompare
from app.config import PAST_DAYS_USED_TO_PREDICT, DAYS_TO_PREDICT, ITERATIONS, MUTATION_WEIGHT, END_TIME

def decision(probability):
    return random.random() < probability
def get_adjusted_data(from_date, to_date, market_1, market_2):
    data = cryptocompare.get_data(
        datetime.timestamp(from_date),
        datetime.timestamp(to_date),
        market_1,
        market_2,
    )

    for d in data:
        d['per_ch'] = (d['close'] - d['open']) / d['open'] * 100.0
        d['volume'] = (d['volumeto'] - d['volumefrom']) / 2
        to_remove = ['volumefrom', 'volumeto', 'conversionType', 'conversionSymbol']
        for r in to_remove:
            del d[r]

    return data

def simulate(from_date, to_date, market_1, market_2):
    data = get_adjusted_data(from_date, to_date, market_1, market_2)
    df = pd.DataFrame(data)

    day = END_TIME
    for days in range(DAYS_TO_PREDICT):
        print(f'Simulating: {day}')
        analysis_data = df.tail(PAST_DAYS_USED_TO_PREDICT).drop(columns=['time'])
        analysis_data_means = analysis_data.mean()

        percentage_change = np.mean(np.absolute(analysis_data['per_ch']))
        increase_probability = np.mean([1 if x > 0 else 0 for x in analysis_data['per_ch']])

        simulation_data = analysis_data.iloc[0:0,:].copy()
        for iteration in range(ITERATIONS):
            should_increase = decision(increase_probability)
            mutation = (1 if should_increase else -1) * random.random() * MUTATION_WEIGHT
            predicted_values = analysis_data_means * (1 + percentage_change * mutation / 100)

            predicted_values['per_ch'] = (predicted_values['close'] - predicted_values['open']) / predicted_values['open'] * 100.0

            simulation_data = simulation_data.append(predicted_values, ignore_index = True)
        print('Mean:')
        print(simulation_data.mean())
        print('Median:')
        median = simulation_data.median()
        print(median)
        print('Deviation:')
        print(simulation_data.std())

        median['time'] = datetime.timestamp(day)
        df = df.append(median, ignore_index = True)
        day += timedelta(days=1)
    return df
