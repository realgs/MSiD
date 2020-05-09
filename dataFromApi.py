import requests
import json
import threading

currencies = ["BTC","ETH","LTC","BCH"]

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

def getData(url, api):
    parsed = parsedData(url)
    print(parsed)
    if api == "bittrex":
        return (parsed["result"]["buy"],parsed["result"]["sell"])
    else:
        return (parsed["bids"],parsed["asks"])
    
def fetchData(api, currency):
    if api == "bitbay":
        return getData("https://bitbay.net/API/Public/{}USD/orderbook.json".format(currency),api)
    if api == "binance":
        return getData("https://api.binance.com/api/v3/depth?symbol={}TUSD".format(currency),api)
    if api == "kraken" and currency == "BTC":
        return getData("https://api.kraken.com/0/public/Depth?pair=XBTUSD".format(currency),api)
    elif api == "kraken":
        return getData("https://api.kraken.com/0/public/Depth?pair={}USD".format(currency),api)
    if api == "bittrex":
        return getData("https://api.bittrex.com/api/v1.1/public/getorderbook?market=USD-{}&type=both".format(currency),api)

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
    print(parsedData("https://api.kraken.com/0/public/Depth?pair=BCHUSD"))
    #printOfferList("Sell","Sell",data[1])
    #print(data[1][0])