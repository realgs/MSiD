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

def fetch_data(currency, startTime, endTime, step, limit):
    data = req.get("https://www.bitstamp.net/api/v2/ohlc/{0}/".format(currency), params={'start': startTime, 'end': endTime, 'step': step, 'limit': limit})
    return data.json()['data']['ohlc']

def parse_data(rawData):
    output = []
    for d in rawData:
        entry = {}
        entry['timestamp'] = d['timestamp']
        entry['diff'] = float(d['close'])-float(d['open'])
        entry['volume'] = d['volume']
        output.append(entry)
    return output

data = fetch_data("btcusd", 1591040415, 1591440415, 86400, 50)
parsed = parse_data(data)
for p in parsed:
    print(p)
