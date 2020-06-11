from datetime import datetime
from datetime import timezone
from datetime import timedelta
from pprint import pprint
from random import choices
from random import randint
import tensorflow
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import time

currency_pairs = ["btcusd", "ltcusd", "ethusd"] 
scaler = MinMaxScaler(feature_range=(0, 1))


def convert_date_to_utc(year, month, day, hour=0, minutes=0, seconds=0):
    dt = datetime(year, month, day, hour, minutes, seconds)
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    return int(timestamp)


def getData(currency_pair, start, end, step):
    limit = (end - start) // step + 1
    if limit > 1000:
        limit = 1000
    bitstamp_data = requests.get("https://www.bitstamp.net/api/v2/ohlc/{0}/".format(currency_pair),
                                 params={'start': start, 'end': end, 'step': step, 'limit': limit})
    if bitstamp_data.status_code == 200:
        bitstamp_data_json = bitstamp_data.json()
        return True, bitstamp_data_json['data']['ohlc']
    else:
        return False, None


def prepareData(oldData):
  data = pd.json_normalize(oldData)
  previous_data_len = len(data)
  for i in range(previous_data_len):
      data.loc[i, 'timestamp'] = datetime.fromtimestamp(int(data.loc[i, 'timestamp']))
  data.rename(columns={'timestamp':'date'}, inplace=True)

  new_data = pd.DataFrame(index=range(0,len(data)), columns=['Date', 'Close'])
  data_simulated = pd.DataFrame(index=range(0,len(data)), columns=['Date', 'Predicted_Close'])
  for i in range(len(data)):
      new_data['Date'][i] = data['date'][i]
      new_data['Close'][i] = float(data['close'][i])
      data_simulated['Date'][i] = data['date'][i] + timedelta(days=len(data))
      data_simulated['Predicted_Close'][i] = 0.0 

  new_data.index = new_data.Date
  data_simulated.index = data_simulated.Date
  new_data.drop('Date', axis=1, inplace=True)
  data_simulated.drop('Date', axis=1, inplace=True)
  dataset = new_data.values
  dataset_simulated = data_simulated.values
  return dataset, data_simulated, new_data


def makeModel(dataset, dataset_simulated):
  x_train, y_train = [], []
  train_index = int(len(dataset)/5*4)
  train = dataset
  valid = dataset_simulated
  scaled_data = scaler.fit_transform(dataset)

  for i in range(60, len(train)):
      x_train.append(scaled_data[i-60:i,0])
      y_train.append(scaled_data[i,0])
  x_train, y_train = np.array(x_train), np.array(y_train)
  x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

  model = Sequential()
  model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
  model.add(LSTM(units=50))
  model.add(Dense(1))

  model.compile(loss='mean_squared_error', optimizer='adam')
  model.fit(x_train, y_train, epochs=5, batch_size=1, verbose=2)
  return model, train, valid
    

def simulate(model, new_data, valid, data_simulated):
  inputs = new_data[len(new_data) - len(valid) - 60:].values
  inputs = inputs.reshape(-1,1)
  inputs = scaler.transform(inputs)

  X_test = []
  X_test.append(inputs)
  X_test = np.array(X_test)
  X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))

  simulation_output = []

  for i in range(len(new_data)):
    if i % randint(3,6) == 0:
      predicted_price = differenceFunc(X_test)
    else:
      predicted_price = model.predict(X_test)
    for j in range(1, 60):
      X_test[0,j-1] = X_test[0,j]
    X_test[0,59] = predicted_price
    simulation_output.append(predicted_price)

  train = new_data
  valid = data_simulated

  converted_output = []
  for i in range(len(simulation_output)):
    converted_output.append([simulation_output[i].item()])

  converted_output = scaler.inverse_transform(converted_output)
  valid['Predicted_Close'] = converted_output
  return train, valid


def differenceFunc(array):
  diff = 0.0
  for i in (30, len(array)):
    diff += array[0,i]/array[0,i+1] - 1
  diff /= (len(array) - 30)
  diff_mults = [10,20,25,30,35,40,45,50,60]
  mult_weights = [0.3, 0.2, 0.15, 0.1, 0.1, 0.05, 0.04, 0.04, 0.02]
  if diff > 0.003:
    return array[0,-1] - array[0,-1]*0.005*choices(diff_mults, mult_weights)
  return array[0,-1] + array[0,-1]*0.005*choices(diff_mults, mult_weights)


def plotResults(x, y, currency_index):
  plt.figure(figsize=(14,10))
  plt.plot(x['Close'])    #train
  plt.plot(y['Predicted_Close'])  #valid
  plt.title(currency_pairs[currency_index])
  plt.gcf().autofmt_xdate()
  plt.show()


def getParameters():
  currency = int(input("Please, enter the number of currency [0 - BTC-USD, 1 - LTC-USD, 2 - ETH-USD]: "))
  date1 = input("Please, enter -date from- in format YYYY-MM-DD: ")
  date2 = input("Please, enter -date to- in format YYYY-MM-DD: ") 
  return currency, convert_date_to_utc(int(date1[0:4]), int(date1[5:7]), int(date1[8:10])), convert_date_to_utc(int(date2[0:4]), int(date2[5:7]), int(date2[8:10]))

def main():
  currency_index, date_from, date_to = getParameters()
  passed, oldData = getData(currency_pairs[currency_index], start=date_from, end=date_to, step=86400)
  dataset, data_simulated, new_data = prepareData(oldData)
  model, train, valid = makeModel(dataset, data_simulated)
  train, valid = simulate(model, new_data, valid, data_simulated)
  plotResults(train, valid, currency_index)


if __name__ == "__main__":
    main()