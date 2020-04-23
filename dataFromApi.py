import requests
import json
import threading

def parsedData(url):
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)
    return parsed

def printOfferList(list):
    for elem in list:
        print("Rate: " + str(elem[0]) + " Amount of Cryptocurrency: " + str(elem[1]))


def main():
    url = "https://bitbay.net/API/Public/BTC/orderbook.json"
    parsed = parsedData(url)
    buy_list = parsed["bids"]
    sell_list = parsed["asks"]
    print("BUY OFFERS")
    printOfferList(buy_list)
    print("SELL OFFERS")
    printOfferList(sell_list)
    best_buy_offer = buy_list[0][0]
    best_sell_offer = sell_list[0][0]
    print((best_sell_offer - best_buy_offer) / (best_buy_offer) * 100)

if __name__ == "__main__":
    main()