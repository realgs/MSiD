import requests
import json
import threading

currencies = ["BTC","ETH","LTC","BCH"]
apis = ["bitbay","binance","kraken", "bitrex"]
wallet = 10000

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

def getData(url, api,currency):
    parsed = parsedData(url)
    
    if api == "bittrex":
        return (parsed["result"]["Bid"],parsed["result"]["Ask"])
    elif api == "kraken":
        if currency == "BTC":
            return (parsed["result"]["XXBTZUSD"]["b"][0],parsed["result"]["XXBTZUSD"]["a"][0])
        elif currency == "BCH":
            return (parsed["result"]["BCHUSD"]["b"][0],parsed["result"]["BCHUSD"]["a"][0])
        else:
            return (parsed["result"]["X"+currency+"ZUSD"]["b"][0],parsed["result"]["X"+currency+"ZUSD"]["a"][0])
    if api == "bitbay":
        return (parsed["bid"],parsed["ask"])
    elif api == "binance":
        return (parsed["bidPrice"],parsed["askPrice"])
    
def fetchData(api, currency):
    if api == "bitbay" and currency == "BCH":
        currency = "BCC"
    if api == "bitbay":
        return getData("https://bitbay.net/API/Public/{}USD/ticker.json".format(currency),api, currency)
    if api == "binance":
        return getData("https://api.binance.com/api/v3/ticker/bookTicker?symbol={}TUSD".format(currency),api, currency)
    if api == "kraken" and currency == "BTC":
        return getData("https://api.kraken.com/0/public/Ticker?pair=XBTUSD".format(currency),api, currency)
    elif api == "kraken":
        return getData("https://api.kraken.com/0/public/Ticker?pair={}USD".format(currency),api, currency)
    if api == "bittrex":
        return getData("https://api.bittrex.com/api/v1.1/public/getticker?market=USD-{}".format(currency),api, currency)

def format(buy_and_sell):
    return (float(buy_and_sell[0]),float(buy_and_sell[1]))
    
            
    

def checkArbitrage():
    for currency in currencies:
        bitbayData = format(fetchData("bitbay", currency))
        binanceData = format(fetchData("binance", currency))
        krakenData = format(fetchData("kraken", currency))
        bittrexData = format(fetchData("bittrex", currency))
        print(bitbayData)
        print(binanceData)
        print(krakenData)
        print(bittrexData)
        

def runMainEvery5Seconds():
    try:
        threading.Timer(5.0, runMainEvery5Seconds).start()
        main()
        print("CTRL+C TO STOP")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    #runMainEvery5Seconds()
    #data = fetchData("kraken", "USD","BTC")
    #print(parsedData("https://bitbay.net/API/Public/BTCUSD/ticker.json"))
    #print(parsedData("https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCTUSD"))
    #print(parsedData("https://api.kraken.com/0/public/Ticker?pair=XBTUSD"))
    #print(parsedData("https://api.bittrex.com/api/v1.1/public/getticker?market=USD-BTC"))
    #printOfferList("Sell","Sell",data[1])
    #print(data[1][0])
    checkArbitrage()