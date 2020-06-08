import requests
import json
import time

criptoCurrencies =[
    "BTC", #Bitcoin
    "ETH", #Ethereum
    "DASH", #Dash
    "GNT",#Golem
    "BCC", #Bitcoin cash
    "LSK", #Lisk
    "BTG", #Bitcoin gold
    "LTC", #Litecoin
    "GAME",  #Gamecredits
]
criptoCurrenciesNames = [
    "Bitcoin",
    "Ethereum",
    "Dash",
    "Golem",
    "Bitcoin cash",
    "Lisk",
    "Bitcoin gold",
    "Litecoin",
    "Gamecredits"
]
def getCurrentAskBid():
    to_ret = ""
    counter = 0
    for currency in criptoCurrencies:
        arrAskBid = getArrBidAsk(currency)
        to_ret += criptoCurrenciesNames[counter]  + " bid: " + str(arrAskBid[0]) + " ask: " + str(arrAskBid[1]) +" in USD"+ "\n"
        counter+=1
    print(to_ret)
def getArrBidAsk(currency):
    url = "https://bitbay.net/API/Public/" + currency + "USD/" + "ticker.json"
    json_obj = requests.get(url)
    json_obj_text = json_obj.text
    parsed_string = json.loads(json_obj_text)
    return [parsed_string["bid"], parsed_string["ask"]]

def diffenceBidAsk():
    while True:
        to_ret = ""
        count = 0
        for currency in criptoCurrencies:
            arrBidAsk = getArrBidAsk(currency)
            proc =  (arrBidAsk[1] - arrBidAsk[0])/arrBidAsk[0]
            proc = round(proc, 2)
            #to_ret+=criptoCurrenciesNames[count] + ": " + round(proc, 2) + "%\n"
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            to_ret += criptoCurrenciesNames[count]+ ": " + "difference in procent: " + str(proc) +"% current time: "+ current_time + "\n"
            count+=1
        print(to_ret)
        time.sleep(5)
#getCurrentAskBid()
diffenceBidAsk()