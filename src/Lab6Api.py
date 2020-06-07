import requests
import matplotlib.pyplot
from datetime import datetime
import time
import random

INPUT_LENGTH = 5
SSS = 500 #Single Simulation Steps
SS = 5 #Simulation steps (how many simulations will be done)
START_DATE = '2019-12-01'
END_DATE = '2020-02-01'
apiCurrencies = ['BTCUSDT', 'ETHBTC', 'LTCBTC']

def getData(startDate, endDate, symbol):
    sTimeStamp = time.mktime(datetime.strptime(startDate,"%Y-%m-%d").timetuple())*1000
    eTimeStamp = time.mktime(datetime.strptime(endDate, "%Y-%m-%d").timetuple())*1000
    deltaTimeStamp = 1000000000
    data = []
    previousTimeStamp = sTimeStamp
    for i in range(int(eTimeStamp-sTimeStamp)//deltaTimeStamp):
        currentTimeStamp = sTimeStamp+(i+1)*deltaTimeStamp
        request = requests.get('https://api.binance.com/api/v3/klines',
            params={'symbol':symbol,'interval':'1h','startTime':str(int(previousTimeStamp)),'endTime':str(int(currentTimeStamp)),'limit':'1000'})
        previousTimeStamp = currentTimeStamp
        data= data + request.json()

    request = requests.get('https://api.binance.com/api/v3/klines',
            params={'symbol': symbol, 'interval': '1h', 'startTime': str(int(previousTimeStamp)),'endTime': str(int(currentTimeStamp)), 'limit': '1000'})
    data = data + request.json()
    return data


print("bip")
print(getData(START_DATE,END_DATE,'BTCUSDT')  )
print("boop - gotowe")