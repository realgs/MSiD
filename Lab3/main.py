import requests
from random import randint
#use to get all market names
markets = requests.get("https://api.bittrex.com/api/v1.1/public/getmarkets").json()['result']
#max requests per minute = 60. 5 requests every 5 seconds is 5*12 = 60 requests every minute.
maxRandomMarkets = 5
namesList = []

for m in markets:
    namesList.append(m['MarketName'])

namesTemp = namesList.copy()
outputNames = []

for i in range(0, maxRandomMarkets):
    index = randint(0, len(namesTemp))
    name = namesTemp[index]
    outputNames.append(name)
    namesTemp.remove(name)


print(f"-------------------------------------------------\n|  Nazwa  |   Sprzedaż   |  Kupno  |  Różnica  |\n-------------------------------------------------")
for name in outputNames:
    prices = requests.get(f"https://api.bittrex.com/api/v1.1/public/getticker?market={name}").json()['result']
    bid = float(prices['Bid'])
    ask = float(prices['Ask'])
    diff = ((ask - bid)/ask) * 100
    print(f"{name:10}  {bid:.8f}   {ask:.8f}   {diff:.4f} %")