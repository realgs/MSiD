import requests
import time
import json

url= "https://api.bittrex.com/api/v1.1/public/getorderbook?market=BTC-LTC&type=both"


headers= {'content-type': 'application/json'}
def operate():
    response = requests.request("GET", url, headers=headers).json()
    while True:
        for el in response["result"]["buy"]:
            print("Buy ")
            print(el["Quantity"]*el["Rate"])
        for el in response["result"]["sell"]:
            print("Sell ")
            print(el["Quantity"]*el["Rate"])
        
        time.sleep(5)
operate()