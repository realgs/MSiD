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

def main():
    url = "https://bitbay.net/API/Public/BTC/orderbook.json"
    parsed = parsedData(url)
    buy_list = parsed["bids"]
    sell_list = parsed["asks"]
    printOfferList("Buy","BUY OFFERS",buy_list)
    printOfferList("Sell", "SELL OFFERS",sell_list)
    getDiffPercentage()
    
def runMainEvery5Seconds():
    try:
        threading.Timer(5.0, runMainEvery5Seconds).start()
        main()
        print("CTRL+C TO STOP")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    runMainEvery5Seconds()