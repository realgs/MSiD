import requests
import threading

# APIs used:
# https://bitbay.net/en/public-api
# https://bittrex.github.io/api/v1-1
# https://cex.io/rest-api#public-api-calls
# https://docs.bitfinex.com/reference#rest-public-ticker

class PriceFetcher(threading.Thread):
    def __init__(self, name, fetchFun):
        threading.Thread.__init__(self)
        self.name = name
        self.value = None
        self.fetchFun = fetchFun

    def run(self):
        self.value = self.fetchFun(self.name)

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
        th = PriceFetcher(m, fetchBitfinexPrice)
        threads.append(th)
        th.start()
    output = []
    for th in threads:
        output.append(th.join())
    return output
        
def fetchBittrexPrice(market):
    prices = requests.get(f"https://api.bittrex.com/api/v1.1/public/getticker?market={market}").json()['result']
    bid = float(prices['Bid'])
    ask = float(prices['Ask'])
    return [market, bid, ask]

def fetchCexPrice(market):
    curr = market.split("-")
    prices = requests.get(f"https://cex.io/api/ticker/{curr[1]}/{curr[0]}")
    prices = prices.json()
    bid = float(prices['bid'])
    ask = float(prices['ask'])
    return [market, bid, ask]

def fetchBitfinexPrice(market):
    curr = market.split("-")
    prices = requests.get(f"https://api-pub.bitfinex.com/v2/ticker/t{curr[1]}{curr[0]}")
    prices = prices.json()
    bid = float(prices[0])
    ask = float(prices[2])
    return [market, bid, ask]

def fetchBitbayPrice(market):
    curr = market.replace("USD","").replace("-","")
    prices = requests.get(f"https://bitbay.net/API/Public/{curr}/ticker.json")
    prices = prices.json()
    bid = float(prices['bid'])
    ask = float(prices['ask'])
    return [market, bid, ask]

