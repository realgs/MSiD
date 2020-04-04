import requests
import json

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
        arrAskBid = getStepString(currency)
        to_ret += criptoCurrenciesNames[counter]  + " bid: " + str(arrAskBid[0]) + " ask: " + str(arrAskBid[1]) +" in USD"+ "\n"
        counter+=1
    print(to_ret)
def getStepString(currency):
    url = "https://bitbay.net/API/Public/" + currency + "USD/" + "ticker.json"
    json_obj = requests.get(url)
    json_obj_text = json_obj.text
    parsed_string = json.loads(json_obj_text)
    return [parsed_string["bid"], parsed_string["ask"]]


getCurrentAskBid()