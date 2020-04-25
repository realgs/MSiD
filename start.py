import requests
import time
import json

BITCOIN =  "btcusd"
LITECOIN = "ltcusd"
ETHEREUM = "ethusd"
URL = "https://api.bitfinex.com/v1/trades/"

def show(currency, data):
    buyVal = 0
    sellVal = []

    print("\n------------")
    print("Cash: " + currency)

    print("<List of purchase offers>")
    for id in range( len(data) ):
        if (data[id]['type'] == "buy"):
            print(round(float(data[id]['price']), 2))
            buyVal = round(float(data[id]['price']), 2)
        else:
            sellVal.append(round(float(data[id]['price']), 2))

    print("\n<List of sale offers>")
    for idd in range(len(sellVal)):
        print(sellVal[idd])

    if(len(sellVal) == 0): sellVal = 0
    print("\n<Subtraction in percents: " + str( round( (((sellVal[0] - buyVal) / buyVal) * 100), 2)) + "%>")


if __name__ == "__main__":

    currencies = [BITCOIN, LITECOIN, ETHEREUM]

    while(True):

        for crypto in range( len(currencies) ):
            address = URL + currencies[crypto]
            response = requests.request("GET", address)

            data = response.json()
            show(currencies[crypto], data)

        time.sleep(5)

