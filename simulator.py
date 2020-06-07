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

def nearest_neighbours(data):
    pass

def distance(dataRow1, dataRow2):
    dist = 0.0
    dist+=(dataRow1['timestamp'] - dataRow2['timestamp'])**2
    dist+=(dataRow1['close'] - dataRow2['close'])**2
    dist+=(dataRow1['open'] - dataRow2['open'])**2
    dist+=(dataRow1['volume'] - dataRow2['volume'])**2
    dist+=(dataRow1['low'] - dataRow2['low'])**2
    dist+=(dataRow1['high'] - dataRow2['high'])**2
    return dist**(1/2)


def predict_direction(data):
    pass

def predict_value(data):
    pass

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

data = fetch_data("btcusd", 1591040415, 1591440415, 86400, 50)
parsed = parse_data(data)
for p in parsed:
    print(p)
plotter(parsed)