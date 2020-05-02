import requests
import threading

# APIs used:
# https://bitbay.net/en/public-api
# https://bittrex.github.io/api/v1-1
# https://cex.io/rest-api
# https://docs.bitfinex.com/reference !limit 30 requests per minute!

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


class MarketInfo():
    def __init(self, currency):
        self.market = ""
        self.currency = currency
        self.bids = []
        self.asks = []
        self.lowSell = []
        self.highBuy = []

def fetchPrices(market):
    threads = []
    fetchFunctions = [fetchBittrexOrders, fetchCexPrice, fetchBitfinexPrice, fetchBitbayPrice]
    for f in fetchFunctions:
        th = PriceFetcher(market, f)
        threads.append(th)
        th.start()
    output = []
    for th in threads:
        output.append(th.join())
    return output
        
def fetchBittrexOrders(market):
    orders = requests.get(f"https://api.bittrex.com/api/v1.1/public/getorderbook?market={market}&type=both").json()['result']
    buy = []
    for o in orders['buy']:
        buy.append([float(o['Quantity']), float(o['Rate'])])
    sell = []
    for o in orders['sell']:
        sell.append([float(o['Quantity']), float(o['Rate'])])
    output = MarketInfo(market)
    output.market = "Bittrex"
    output.bids = buy
    output.asks = sell
    return output

def fetchCexPrice(market):
    curr = market.split("-")
    orders = requests.get(f"https://cex.io/api/order_book/{curr[1]}/{curr[0]}?depth=100").json()
    buy = []
    for o in orders['bids']:
        buy.append([float(o[1]), float(o[0])])
    sell = []
    for o in orders['asks']:
        sell.append([float(o[1]), float(o[0])])
    output = MarketInfo(market)
    output.market = "CEX.IO"
    output.bids = buy
    output.asks = sell
    return output

def fetchBitfinexPrice(market):
    curr = market.split("-")
    orders = requests.get(f"https://api-pub.bitfinex.com/v2/book/t{curr[1]}{curr[0]}/P0?len=100").json()
    buy = []
    sell = []
    for o in orders:
        rate, quantity = float(o[0]), float(o[2])
        if quantity > 0:
            buy.append([quantity, rate])
        else:
            sell.append([quantity, rate])

    output = MarketInfo(market)
    output.market = "Bitfinex"
    output.bids = buy
    output.asks = sell
    return output

def fetchBitbayPrice(market):
    curr = market.replace("USD","").replace("-","")
    orders = requests.get(f"https://bitbay.net/API/Public/{curr}/orderbook.json").json()
    buy = []
    for o in orders['bids']:
        buy.append([float(o[1]), float(o[0])])
    sell = []
    for o in orders['asks']:
        sell.append([float(o[1]), float(o[0])])
    output = MarketInfo(market)
    output.market = "Bitbay"
    output.bids = buy
    output.asks = sell
    return output