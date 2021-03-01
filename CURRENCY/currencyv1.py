import requests
import time

import json

url = "https://api.bitbay.net/rest/trading/transactions/BTC-PLN"
url2 = "https://api.bitbay.net/rest/trading/ticker/BTC-PLN"
headers = {'content-type': 'application/json'}
def operate():
    while True:
        response = requests.request("GET", url, headers=headers).json()
        statistic=requests.request("GET", url2, headers=headers).json()
        
        for a in response['items']:
            print(" Kwota transakcji "+str(float(a['a'])*float(a['r']))+ "zł typ transakcji "+ a['ty'] )
            if a['ty']=="Sell":
                print ("przelicznik oferty względem kupna "+str(1-(float(a["r"])-float(statistic['ticker']['highestBid']))/float(statistic['ticker']['highestBid'])))
            if a['ty']=="Buy":
                print ("przelicznik oferty względem sprzedaży "+str(1-(float(a["r"])-float(statistic['ticker']['lowestAsk']))/float(statistic['ticker']['lowestAsk'])))
            

        time.sleep(5)

def show_Full_offers():
    response = requests.request("GET", url, headers=headers).json()
    for el in response["items"]:
        print (el)
    

show_Full_offers()
operate()

