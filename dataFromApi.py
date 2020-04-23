import requests
import json

url = "https://bitbay.net/API/Public/BTC/orderbook.json"
response = requests.get(url)

data = response.text

parsed = json.loads(data)

buy_list = parsed["bids"]
sell_list = parsed["asks"]

print(len(buy_list))
print(len(sell_list))

print("BUY LIST")

for buy in buy_list:
    print("RATE: " + str(buy[0]) + " AMOUNT OF CRYPTOCURRENCY: " + str(buy[1]))

print("SELL LIST")

for sell in sell_list:
    print("RATE: " + str(sell[0]) + "AMOUNT OF CRYPTOCURRENCY: " + str(sell[1]))

best_buy_offer = buy_list[0][0]
best_sell_offer = sell_list[0][0]

print((best_sell_offer - best_buy_offer) / (best_buy_offer) * 100)