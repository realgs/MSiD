import requests
import datetime
import time

CURRENCIES = ['BTC','BCC','LTC', 'ETH']
AMOUNTOFOFFERS = 3
def printOffers(amount, currency, bid, ask):
    print(currency +" buy/sell = {}%".format(str(round((1-(ask[0][0]-bid[0][0])/ask[0][0]),4))))
    print("bids offers:\tasks offers")
    print("{0}:USD\t\t\t{0}:USD".format(currency))
    for i in range(amount):
        print(str(bid[i][0])+"\t\t\t"+str(ask[i][0]))
    print()

while True:
    x = datetime.datetime.now()
    print(x)
    for currency in CURRENCIES:
        requestLink = 'https://bitbay.net/API/Public/{}/orderbook.json'.format(currency)
        respons = requests.get(requestLink)
        printOffers(AMOUNTOFOFFERS,currency,respons.json()["bids"],respons.json()["asks"])
    print("\n")
    time.sleep(10)