import requests
import json
import time
import os


def cls(): os.system('cls' if os.name == 'nt' else 'clear')


def calculateDiff(sell_price, buy_price):
    if sell_price == None or buy_price == None:
        return -1
    return  (float(sell_price) - float(buy_price)) / float(buy_price)*100


def loadFromApi():
    url = 'https://api.bitbay.net/rest/trading/ticker'
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text)


def currencyMonitor(markets):
    while True:
        response_dict = loadFromApi()
        cls()
        for market in markets:
            diff = calculateDiff(response_dict['items'][market]['lowestAsk'], response_dict['items'][market]['highestBid'])
            print("Market: {0:15} Bid: {1:15}\tAsk: {2:15}Difference: {3:.2f} %".
                format(market, str(response_dict['items'][market]['highestBid']), str(response_dict['items'][market]['lowestAsk']), diff))
        time.sleep(5)

def main():
    markets_list = ("BTC-PLN","BTC-USD","ETH-USD","LTC-USD","LSK-USD","BCC-USD","DASH-USD")
    currencyMonitor(markets_list)


if __name__ == "__main__":
    main()