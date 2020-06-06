#fetch data - DONE
#parse data
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
    return data.json()

print(fetch_data("btcusd", 1591040415, 1591440415, 259200, 1000))