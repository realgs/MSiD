import requests
import time
import datetime

s = "03/06/2020"
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
        data_day.append((dataset[i-1][3] - float(record[6]))/float(record[6]))
    else:
        data_day.append(0)
    data_day.append(float(record[4]))
    data_day.append(float(record[6]))
    data_day.append(float(record[4])/float(record[6]))
    dataset.append(data_day)
    i = i+1
print(dataset)