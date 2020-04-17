import requests
import threading

#threadLock = threading.Lock()

class PriceFetcher(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.value = None

    def run(self):
        #threadLock.acquire()
        prices = requests.get(f"https://api.bittrex.com/api/v1.1/public/getticker?market={self.name}").json()['result']
        bid = float(prices['Bid'])
        ask = float(prices['Ask'])
        #threadLock.release()
        self.value = [self.name, bid, ask]

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self.value

def fetchMarkets():
    markets = requests.get("https://api.bittrex.com/api/v1.1/public/getmarkets").json()['result']
    output = []
    for m in markets:
        output.append(m['MarketName'])
    return output

def fetchPrices(markets):
    threads = []
    for m in markets:
        th = PriceFetcher(m)
        threads.append(th)
        th.start()
    output = []
    for th in threads:
        output.append(th.join())
    return output
        
