import requests
import time
import json


urlBTC_LTC= "https://poloniex.com/public?command=returnOrderBook&currencyPair=BTC_LTC&depth=50"
urlBTC_ETH= "https://poloniex.com/public?command=returnOrderBook&currencyPair=BTC_ETH&depth=50"
urlETH_LTC= "https://poloniex.com/public?command=returnOrderBook&currencyPair=ETH_USD&depth=50"
urlLTC_XML= "https://poloniex.com/public?command=returnOrderBook&currencyPair=LTC_XML&depth=50"
curl= "https://poloniex.com/public?command=returnCurrencies"
sellBTC_LTC=[]
sellBTC_ETH=[]
sellETH_LTC=[]
sellLTC_XML=[]
buyBTC_LTC=[]
buyBTC_ETH=[]
buyETH_LTC=[]
buyLTC_XML=[]
headers= {'content-type': 'application/json'}
def operatePOL(sell,buy,url):
    sell.clear()
    buy.clear()
    response = requests.request("GET", url, headers=headers).json()
    for el in response["asks"]:
        sell.append(el)
    for el in response["bids"]:
        buy.append(el)
    
def processPOL():
    operatePOL(sellBTC_LTC, buyBTC_LTC, urlBTC_LTC)
    operatePOL(sellBTC_ETH, buyBTC_ETH, urlBTC_ETH)
    operatePOL(sellETH_LTC, buyETH_LTC, urlETH_LTC)
    operatePOL(sellLTC_XML, buyLTC_XML, urlLTC_XML)
    
    
res = requests.request("GET", curl, headers=headers).json()
for el in res:
    print(el)



