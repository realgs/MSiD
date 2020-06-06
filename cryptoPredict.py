import requests
import time
import datetime
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

s = "01/06/2020"
t = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())
parameters = {"pair": "XBTUSD", "interval": 1440, "since": t}
response = requests.get("https://api.kraken.com/0/public/OHLC", params = parameters)
data = response.json()
result = data['result']['XXBTZUSD']
dataset = []
i = 0
for record in result:
    data_day = []
    data_day.append((float(record[4]) - float(record[1]))/float(record[1])) 
    if i > 0:
        data_day.append((dataset[i-1][7] - float(record[6]))/dataset[i-1][7])
    else:
        data_day.append(0)
    if data_day[0] > 0:
        data_day.append(1)
        data_day.append(0)
    else:
        data_day.append(0)
        data_day.append(1)
    if data_day[1] > 0:
        data_day.append(1)
        data_day.append(0)
    else:
        data_day.append(0)
        data_day.append(1)
    data_day.append(float(record[4]))
    data_day.append(float(record[6]))
    data_day.append(float(record[4])/float(record[6]))
    dataset.append(data_day)
    i = i+1

D = np.matrix(dataset)
D = np.squeeze(np.asarray(D))
y = D[1:,[0,1,2,3,4,5]]
X = D[:-1,[0,1,6,7,8]]
print(X)
print(y)
regressor = LinearRegression()
model = regressor.fit(X, y)
print(model.coef_)




