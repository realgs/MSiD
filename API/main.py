import requests
import json
import time 
currenciesToDownload = ["USD-KMD", "USD-USDC", "USD-TUSD", "USD-HBAR","USD-BTC", "USD-ETH"]

class Currency:
    name = ""
    sellPrice = ""
    buyPrice = ""

    def __init__(self, name, buyPrice, sellPrice):
        self.name = name
        self.sellPrice = sellPrice
        self.buyPrice = buyPrice
    
    def __str__(self):
        return self.name + " SELL: " + str(self.sellPrice) + "| BUY:" + str(self.buyPrice)


def apiQuery(url, nameOfCurrency):
    response = requests.get(url + nameOfCurrency)
    json_data = response.json()
    return json_data


def retriveDataToCurrency(jsonResponse, currencyName):
    if jsonResponse is not None:
        buyPrice = jsonResponse['result']['Ask']
        sellPrice = jsonResponse['result']['Bid']
        currency = Currency(currencyName, buyPrice, sellPrice)
        return currency
    return None

def downloadDataAboutCurrencies(listOfCurrencies):
    for currency in currenciesToDownload:
        jsonResponse = apiQuery("https://api.bittrex.com/api/v1.1/public/getticker?market=", currency)
        currency = retriveDataToCurrency(jsonResponse, currency)
        listOfCurrencies.append(currency)


def main():
    listOfCurrencies = []
    downloadDataAboutCurrencies(listOfCurrencies)
    
    for currency in listOfCurrencies:
        print(currency)
        percantageDiff = (1 - (currency.buyPrice - currency.sellPrice) / currency.sellPrice)
        print("Diffrence percantage for " + currency.name + ": " + str(percantageDiff))
    print('---------------------------------')
    time.sleep(5.0)
    main()

    
main()

