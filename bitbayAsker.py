import requests
import time

#coins = ['btc', 'bcc','ltc','eth','lsk','game','dash','btg',
#         'kzc','xin','xrp','zec','gnt','omg','fto','rep',
#         'zrx','pay','bat','neu','trx','amlt','exy','bob']



COINS = ['BTC','LTC','ETH']

def print5ClosestOffers(coin, bids, asks):
    print(coin +"    buy/sell = {}%".format(str(round((1-(asks[0][0]-bids[0][0])/asks[0][0]),4))))
    print("bids offers({0}:USD):\t\tasks offers({0}:USD):".format(coin))
    for i in range(5):
        print(str(bids[i][0])+"\t\t\t\t"+str(asks[i][0]))
    print()

while True:
    print(time.asctime( time.localtime(time.time()))+": ")
    for coin in COINS:
        requestFormat = 'https://bitbay.net/API/Public/{}/orderbook.json'.format(coin)
        respons = requests.get(requestFormat)
        print5ClosestOffers(coin,respons.json()["bids"],respons.json()["asks"])
    print("\n")
    time.sleep(5)