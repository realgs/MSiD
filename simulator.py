#fetch data - DONE
#parse data - DONE
#implement knn
#knn to detect fall or rise - look for similiar opens/closes/volumes
#knn to detect how much - look for similiar probabilities
#plot results

#knn references: 
#https://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/
#https://github.com/sammanthp007/Stock-Price-Prediction-Using-KNN-Algorithm

import requests as req
import matplotlib.pyplot as plot
import numpy as np

MAX_NN = 11

def fetch_data(currency, startTime, endTime, step, limit):
    data = req.get("https://www.bitstamp.net/api/v2/ohlc/{0}/".format(currency), params={'start': startTime, 'end': endTime, 'step': step, 'limit': limit})
    return data.json()
#   RAW DATA
#pair	    Trading pair
#high	    Price high
#timestamp	Unix timestamp date and time
#volume	    Volume
#low	    Price low
#close  	Closing price
#open       Opening price
def parse_data(rawData):
    rawData = rawData['data']['ohlc']
    output = []
    for d in rawData:
        entry = {}
        entry['timestamp'] = int(d['timestamp'])
        entry['close'] = float(d['close'])
        entry['open'] = float(d['open'])
        entry['volume'] = float(d['volume'])
        entry['low'] = float(d['low'])
        entry['high'] = float(d['high'])
        output.append(entry)
    return output

def distance(dataRow1, dataRow2):
    dist = 0.0
    dist+=(dataRow1['close'] - dataRow2['close'])**2
    dist+=(dataRow1['open'] - dataRow2['open'])**2
    dist+=(dataRow1['volume'] - dataRow2['volume'])**2
    dist+=(dataRow1['low'] - dataRow2['low'])**2
    dist+=(dataRow1['high'] - dataRow2['high'])**2
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

def predict_linear_numpy(neighbours, timestamp):
    x, y = [], []
    for n in neighbours:
        x.append(n['timestamp'])
        y.append(n['close'])

    x, y = np.array(x), np.array(y)
    A = np.vstack([x, np.ones(len(x))]).T

    b1, b2 = np.linalg.lstsq(A, y)[0]
    return b1 * timestamp + b2

#Least Squares
def predict_linear(neighbours, timestamp):
    x, y = [], []
    for n in neighbours:
        x.append(n['timestamp'])
        y.append(n['close'])

    x, y = np.array(x), np.array(y)

    n = np.size(x) 
    meanX, meanY = np.mean(x), np.mean(y) 
    xySS = np.sum(y * x) - n * meanY * meanX 
    xxSS = np.sum(x * x) - n * meanX * meanX 
    b1 = xySS / xxSS 
    b0 = meanY - b1 * meanX 
  
    return b1 * timestamp + b0

def predict_avg(neighbours):
    y = []
    for n in neighbours:
        y.append(n['close'])
    return np.mean(np.array(y))

def simulate(data):
    pass

def plotter(data):
    timestamps = []
    difs = []
    for d in data:
        timestamps.append(d['timestamp'])
        difs.append(d['diff'])

    plot.plot(timestamps, difs)
    plot.show()

data = fetch_data("btcusd", 1591040415, 1591440415, 86400, 1000)
parsed = parse_data(data)
lastRow = parsed.pop()
nn = nearest_neighbours(parsed, lastRow)
print("For row:")
print(lastRow)
print("NN are:")
for n in nn:
    print(n)
#plotter(parsed)
lnnp = predict_linear_numpy(nn, lastRow['timestamp'])
ln = predict_linear(nn, lastRow['timestamp'])
avg = predict_avg(nn)
print(f"Lin Nump: {lnnp} vs Lin: {ln} vs Avg: {avg}")