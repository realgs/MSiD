import requests as req
import matplotlib.pyplot as plot
import numpy as np
from datetime import datetime

MAX_NN = 11

def fetch_data(currency, startTime, endTime, step, limit):
    data = req.get("https://www.bitstamp.net/api/v2/ohlc/{0}/".format(currency), params={'start': startTime, 'end': endTime, 'step': step, 'limit': limit})
    return data.json()

def parse_data(rawData):
    rawData = rawData['data']['ohlc']
    output = []
    for d in rawData:
        entry = {}
        entry['timestamp'] = int(d['timestamp'])
        entry['close'] = float(d['close'])
        entry['open'] = float(d['open'])
        entry['volume'] = float(d['volume'])
        output.append(entry)
    return output

def distance(dataRow1, dataRow2):
    dist = 0.0
    dist+=(dataRow1['timestamp'] - dataRow2['timestamp'])**2
    dist+=(dataRow1['close'] - dataRow2['close'])**2
    dist+=(dataRow1['open'] - dataRow2['open'])**2
    dist+=(dataRow1['volume'] - dataRow2['volume'])**2
    return dist**(1/2)

def nearest_neighbours(data, predictRow):
    distances = []
    for dataRow in data:
        distances.append((dataRow, distance(dataRow, predictRow)))
    distances.sort(key=lambda tup: tup[1])
    neighbours = []
    for i in range(min(len(distances), MAX_NN)):
        neighbours.append(distances[i][0])
    return neighbours

def predict_avg(neighbours):
    valueDif = []
    volumeAvg = []
    for n in neighbours:
        valueDif.append((n['close']-n['open'])/n['close'])
        volumeAvg.append(n['volume'])
    return np.mean(np.array(valueDif)), np.mean(np.array(volumeAvg))

def simulate(data):
    predictionsData = []
    predictionsData.append(data[0])
    predictions = []
    for i in range(1, len(data)): #len(data) = simulation for historical period data
        nn = nearest_neighbours(data, predictionsData[i-1])
        valueDif, volumeAvg = predict_avg(nn)
        entry = {}
        entry['timestamp'] = data[i]['timestamp']
        entry['volume'] = volumeAvg
        prevClose = predictionsData[i-1]['close']
        entry['open'] = prevClose
        entry['close'] = prevClose + prevClose * valueDif
        predictions.append(entry['close'])
        predictionsData.append(entry)

    data.pop()
    plotter(predictions, data)

def plotter(predictions, data):
    dates = []
    actualValues = []
    for d in data:
        dates.append(d['timestamp'])
        actualValues.append(d['close'])
    plot.plot(dates, predictions, label = "Predicted")
    plot.plot(dates, actualValues, label = "Actual")
    plot.legend()
    plot.show()

data = fetch_data("btcusd", 1591040415, 1591440415, 86400, 1000)
parsed = parse_data(data)
simulate(parsed)