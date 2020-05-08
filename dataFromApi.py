import requests
import json
import threading

def parsedData(url):
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)
    return parsed

def printOfferList(offer_type,list_title, list):
    print(list_title)
    for elem in list:
        print(offer_type + " Rate: " + str(elem[0]) + " Amount of Cryptocurrency: " + str(elem[1]))

def getDiffPercentage(buy_list, sell_list):
    best_buy_offer = buy_list[0][0]
    best_sell_offer = sell_list[0][0]
    print("BUY/SELL PERCENT DIFFERENCE " + str((best_sell_offer - best_buy_offer) / (best_buy_offer) * 100))

def getBitbayData():
    url = "https://bitbay.net/API/Public/BTC/orderbook.json"
    parsed = parsedData(url)
    buy_list = parsed["bids"][0]
    sell_list = parsed["asks"][0]
    return (buy_list, sell_list)

def getBittrexData():
    url = "https://api.bittrex.com/api/v1.1/public/getorderbook?market=USD-BTC&type=both"
    parsed = parsedData(url)
    sell_list = parsed["result"]["sell"]
    buy_list = parsed["result"]["buy"]
    return (buy_list, sell_list)

def getBinanceData():
    url = "https://api.binance.com/api/v3/depth?symbol=BTCTUSD"
    parsed = parsedData(url)
    #print(parsed)
    sell_list = parsed["asks"]
    buy_list = parsed["bids"]
    return (buy_list, sell_list)
    
def getBitstampData():
    url = "https://www.bitstamp.net/api/v2/order_book/BTCUSD/""
    parsed = parsedData(url)
    #print(parsed)
    sell_list = parsed["asks"]
    buy_list = parsed["bids"]
    return (buy_list, sell_list)

def runMainEvery5Seconds():
    try:
        threading.Timer(5.0, runMainEvery5Seconds).start()
        main()
        print("CTRL+C TO STOP")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    runMainEvery5Seconds()