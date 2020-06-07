import requests as req
import matplotlib.pyplot as plot
import numpy as np
from datetime import datetime
import random

MAX_NN = 11
NUM_OF_SIMS = 10
currPairs = ["ltcusd", "btcusd", "ethusd"]
noiseChance = 0.33
noisePercent = 0.40

def fetch_data(currency, startTime, endTime, step):
    limit = min(1000, (endTime-startTime)//step)
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

def simulate_single(data):
    predictionsData = []
    predictionsData.append(data[0])
    predictions = []
    for i in range(1, len(data)): #len(data) = simulation for historical period data
        nn = nearest_neighbours(data, predictionsData[i-1])
        valueDif, volumeAvg = predict_avg(nn)
        if random.random() <= noiseChance:
            valueDif+=valueDif*noisePercent
        entry = {}
        entry['timestamp'] = data[i]['timestamp']
        entry['volume'] = volumeAvg
        prevClose = predictionsData[i-1]['close']
        entry['open'] = prevClose
        entry['close'] = prevClose + prevClose * valueDif
        predictions.append(entry['close'])
        predictionsData.append(entry)

    return predictions
def plotter(single, mean, data):
    data.pop()
    dates = []
    actualValues = []
    for d in data:
        dates.append(datetime.fromtimestamp(d['timestamp']))
        actualValues.append(d['close'])
    print(f"DATES:{len(dates)}, SINGLE:{len(single)}, MEAN:{len(mean)}, ACTUAL:{len(actualValues)}")
    plot.plot(dates, single, label = "Single simulation")
    plot.plot(dates, mean, label = "100 simulations")
    plot.plot(dates, actualValues, label = "Actual data")
    plot.legend()
    plot.show()

def simulation():
    data = fetch_data(currPairs[2], 1561040415, 1591440415, 86400)
    data = parse_data(data)
    singleSim = simulate_single(data)
    hundredSims = []
    for i in range(NUM_OF_SIMS):
        print(f"Simulation {i+1}...")
        hundredSims.append(simulate_single(data))
    meanSim = []
    limit = len(hundredSims[0])
    print(f"LIMIT: {limit}, NUM:{NUM_OF_SIMS}, HUNNUM:{len(hundredSims)}, HUNLIM:{len(hundredSims[0])}")
    for i in range(limit):
        meanSim.append(0)
        for j in range(NUM_OF_SIMS):
            print(f"I: {i}, J: {j}")
            meanSim[i] += hundredSims[j][i]
        meanSim[i] = meanSim[i] / NUM_OF_SIMS
    plotter(singleSim, meanSim, data)
    
simulation()