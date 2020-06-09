from datetime import timezone, datetime
import requests
import matplotlib.pyplot as plt
import numpy as np
import random
import json
import math

K = 40 # Number of analyzed nearest "neighbours"
currency_pair = ["btcusd", "ltcusd", "bchusd"]

def convert_date_to_utc(year, month, day, hour=0, minutes=0, seconds=0):
    dt = datetime(year, month, day, hour, minutes, seconds)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    return int(timestamp)

def convert_utc_to_date(timestamp):
    return datetime.fromtimestamp(timestamp)

def get_data(currency_pair, start, end, step):
    limit = (end - start) // step + 1
    if limit > 1000:
        limit = 1000
    bitstamp_data = requests.get("https://www.bitstamp.net/api/v2/ohlc/{0}/".format(currency_pair),
                                 params={'start': start, 'end': end, 'step': step, 'limit': limit})
    if bitstamp_data.status_code == 200:
        bitstamp_data = bitstamp_data.json()['data']['ohlc']
        data = []
        for unit in bitstamp_data:
            data.append({'close': float(unit['close']), 'volume': float(unit['volume']), 'timestamp': int(unit['timestamp'])})
        return False, data
    else:
        return True, None

def create_model(data):
    unit_prev = data[0]
    model = []
    for unit in data[1:]:
        close_dif = (unit['close'] - unit_prev['close'])
        volume_dif = (unit['volume'] - unit_prev['volume'])
        close_dif_percentage = close_dif / unit_prev['close']
        volume_dif_percentage= volume_dif / unit_prev['volume']
        price_volume_ratio = 1
        if close_dif != 0:
            price_volume_ratio = volume_dif / close_dif

        model.append({
        'close': unit['close'],
        'volume': unit['volume'],
        'timestamp': unit['timestamp'],
        'close_dif_percentage': close_dif_percentage,
        'volume_dif_percentage': volume_dif_percentage,
        'price_volume_ratio': price_volume_ratio
        })
        unit_prev = unit
    return model

def avg(list, key):
    sum = 0.0
    for element in list:
        sum += element[key]
    return sum / len(list)

def med(list, dic_key):
    list.copy().sort(key = lambda i: i[dic_key])
    n = int(len(list))
    if n % 2 == 0:
        return list[int(n/2)][dic_key]
    else:
        return (list[int(n/2)][dic_key] + list[int(n/2)+1][dic_key])/2

def std_dev(list, key):
    average = avg(list, key)
    sum = 0.0
    for element in list:
        sum += math.pow(element[key] - average, 2)
    sum /= len(list)-1
    return math.sqrt(sum)

def replace_worse_neighbour(neighbours, close_dif_percentage, new_neighbour):
    max = close_dif_percentage
    ngh = None
    for neighbour in neighbours:
        if abs(neighbour['close_dif_percentage'] - close_dif_percentage) > max:
            (max, ngh) = (abs(neighbour['close_dif_percentage'] - close_dif_percentage), neighbour)
    if ngh != None:
        neighbours.remove(ngh)
        neighbours.append(new_neighbour)
        return True
    return False

def get_neighbours_successors(model, neighbours):
    neighbours_successors = []
    neighbours.sort(key = lambda i: i['timestamp'])
    for index, unit in enumerate(model):
        if unit == neighbours[0]:
            neighbours_successors.append(model[index+1])
            neighbours.pop(0)
        if len(neighbours) == 0 or index >= len(model)-2:
            return neighbours_successors

def estimate_next_data(model, prev_data, cur_data):
    neighbours = model[0:K]
    close_dif_percentage = (cur_data['close'] - prev_data['close']) / prev_data['close']
    for unit in model[K:]:
        close_unit_dif_percentage = close_dif_percentage - unit['close_dif_percentage']
        replace_worse_neighbour(neighbours, close_unit_dif_percentage, unit)
    neighbours_successors = get_neighbours_successors(model, neighbours)
    probability_close = avg(neighbours_successors, "close_dif_percentage")
    volume_indicator = avg(neighbours_successors, "volume_dif_percentage")
    volume_multiplicator = avg(neighbours_successors, "price_volume_ratio")
    next_data = cur_data.copy()
    next_data["close"] = random.uniform(1-probability_close*5, 1+probability_close*5) * cur_data["close"]
    if volume_indicator > 0:
        next_data["volume"] = volume_indicator * abs(volume_multiplicator)/5 * cur_data["close"]
    else:
        next_data["volume"] = -volume_indicator / abs(volume_multiplicator) * cur_data["volume"]
    return next_data

def simulate_data(model, step):
    cur_timestamp = model[-1]['timestamp']
    simulated_data = []
    prev_data = model[-2]
    cur_data = model[-1]
    iterations = len(model)
    for i in range (0, iterations):
        cur_timestamp += step
        next_data = estimate_next_data(model, prev_data, cur_data)
        next_data['timestamp'] = cur_timestamp
        prev_data = cur_data
        cur_data = next_data
        simulated_data.append(next_data)
        model.append(next_data)
    return simulated_data

def get_list_by_key(data, key):
    return [unit[key] for unit in data]

def show_graph(data, currency_pair, ending_date):
    prices = get_list_by_key(data, 'close')
    volumes = get_list_by_key(data, 'volume')
    timestamps = get_list_by_key(data, 'timestamp')
    date_labels = map(convert_utc_to_date, timestamps)
    date_labels = list(date_labels)

    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(figsize=(15, 8))
    ax1.set_xlabel('date')
    ax1.set_ylim([0, 2 * max(volumes)])
    ax1.bar(date_labels, volumes, color='#FF5D5D', alpha=0.75, width=1)
    ax1.tick_params(axis='y', labelcolor='#000000')
    ax2 = ax1.twinx()
    ax2.set_ylabel('price')
    ax2.plot(date_labels, prices, color="#CDE33B", alpha=0.75)
    ax2.tick_params(axis='y')
    plt.title(currency_pair, fontsize=24)
    plt.axvline(x=convert_utc_to_date(ending_date), color='#00BDD1', alpha=0.5)
    plt.gcf().autofmt_xdate()
    plt.show()

def prepare_model(currency_pair, starting_date, ending_date, step):
    (error, data) = get_data(currency_pair, starting_date, ending_date, step)
    if error is True:
        return
    model = create_model(data)
    return model

def analyze_simulated_data(simulated_data, iterations):
    avg_simulated_data = []
    for unit in simulated_data[0]:
        avg_simulated_data.append({'close': 0.0, 'volume': 0.0, 'timestamp': unit['timestamp']})
    for simulation in simulated_data:
        for index, unit in enumerate(simulation):
            for str in ['close', 'volume']:
                avg_simulated_data[index][str] += unit[str]
        for str in ['close', 'volume']:
            print("  price" if str is 'close' else "  " + str)
            print("    avg: {:.2f} | median: {:.2f} | standard deviation: {:.2f}".format(avg(simulation, str),med(simulation, str), std_dev(simulation, str)))
        print()

    for data in avg_simulated_data:
        for str in ['close', 'volume']:
            data[str] = data[str] / iterations

    return avg_simulated_data

def run_simulation(currency_pair, starting_date, ending_date, step, iterations):
    model = prepare_model(currency_pair, starting_date, ending_date, step)
    simulated_data = []
    for i in range(0,iterations):
        print(f"Iteration: {i+1}")
        simulated_data.append(simulate_data(model.copy(), step))
    avg_simulated_data = analyze_simulated_data(simulated_data, iterations)
    show_graph(model + avg_simulated_data, currency_pair, ending_date)

def main():
    starting_date = convert_date_to_utc(2016, 6, 29)
    ending_date = convert_date_to_utc(2020, 1, 1)
    step = 60 * 60 * 24
    run_simulation(currency_pair[0],starting_date, ending_date, step, 1)
    run_simulation(currency_pair[0],starting_date, ending_date, step, 100)

if __name__ == "__main__":
    main()
