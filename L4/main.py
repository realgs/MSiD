import requests
import json
import time 

bittrex_url = "https://api.bittrex.com/api/v1.1/public/getorderbook?market=USD-{}&type=both" 
cex_url = "https://cex.io/api/order_book/{}/USD?depth=100" 
bitstamp_url = "https://www.bitstamp.net/api/v2/order_book/{}usd"
bitbay_url = "https://bitbay.net/API/Public/{}/orderbook.json" 

bittrexFee = 0.0025
bitstampFee = 0.0025
cexFee = 0.0016
bitbayFee = 0.001 

currenciesToDownload = ["BTC", "ETH", "LTC", "XRP"]

class OrderBook:
    siteName = ""
    listOfOrdersBid = []
    listOfOrdersAsk = []
    minAskPrice = ""
    maxBidPrice = ""
    fee = ""

    def findMinAndMax(self):
        self.minAskPrice = min(self.listOfOrdersAsk, key=lambda currency: currency.rate)
        self.maxBidPrice = max(self.listOfOrdersBid, key=lambda currency: currency.rate)

    def __init__(self, siteName, listOfOrdersBid, listOfOrdersAsk):
        self.siteName = siteName
        self.listOfOrdersBid = listOfOrdersBid
        self.listOfOrdersAsk = listOfOrdersAsk
        if siteName == "bitstamp":
            self.fee = float(bitstampFee)
        elif siteName == "bitbay":
            self.fee = float(bitbayFee)
        elif siteName == "bittrex":
            self.fee = float(bittrexFee)
        elif siteName == "cex":
            self.fee = float(cexFee)
        else: self.fee = 0.0001
        
class Currency:
    rate = ""
    quantity = ""

    def __init__(self, rate, quantity):
        self.rate = rate
        self.quantity = quantity

    def __str__(self):
        return str(self.rate) + " RATE | " + str(self.quantity) + " QUANTITY"

    def __repr__(self):
        return str(self.rate) + " RATE | " + str(self.quantity) + " QUANTITY"

def orderBookFromAPI(url, currency):
    response = requests.get(url.format(currency))
    if response.status_code != 200: return None
    json_data = response.json()
    return json_data

def jsonResponseToOrderBook(orders, siteName):
    if orders is None: return None

    orderBook = OrderBook(siteName, [], [])

    if siteName == "bittrex":
        for bid in orders["result"]["buy"]:
            currency = Currency(float(bid["Rate"]), float(bid["Quantity"]))
            orderBook.listOfOrdersBid.append(currency)
            # sorted(orderBook.listOfOrdersBid, key=lambda currency: currency.rate, reverse= True)
        for ask in orders["result"]["sell"]:
            currency = Currency(float(ask["Rate"]), float(ask["Quantity"]))
            orderBook.listOfOrdersAsk.append(currency)
            # sorted(orderBook.listOfOrdersAsk, key=lambda currency: currency.rate)
    else:
        for bid in orders["bids"]:
            currency = Currency(float(bid[0]), float(bid[1]))
            orderBook.listOfOrdersBid.append(currency)
            # sorted(orderBook.listOfOrdersBid, key=lambda currency: currency.rate, reverse= True)
        for ask in orders["asks"]:
            currency = Currency(float(ask[0]), float(ask[1]))
            orderBook.listOfOrdersAsk.append(currency)
            # sorted(orderBook.listOfOrdersAsk, key=lambda currency: currency.rate)

    orderBook.findMinAndMax()

    return orderBook

def findMax(orderBooks):
    if orderBooks[0] is not None:
        maxOB = orderBooks[0]

    for orderBook in orderBooks:
        if orderBook is not None and maxOB.maxBidPrice.rate < orderBook.maxBidPrice.rate:
            maxOB = orderBook
    return maxOB

def calculateProfit(orderBooks, currencyName, wallet):
    maxSellPriceOrderBook = findMax(orderBooks)

    for orderBook in orderBooks:
        if orderBook is not None:
            if orderBook.minAskPrice.rate < maxSellPriceOrderBook.maxBidPrice.rate:
                quantity = min(orderBook.minAskPrice.quantity, maxSellPriceOrderBook.maxBidPrice.quantity)


                askMoney = (orderBook.minAskPrice.rate * quantity)
                if askMoney <= wallet:
                    bidMoney = (maxSellPriceOrderBook.maxBidPrice.rate * quantity) - (maxSellPriceOrderBook.maxBidPrice.rate * quantity * orderBook.fee)

                    profit = bidMoney - askMoney
                    profit = round(profit, 2)

                    if  profit > 0:
                        print("""Na giełdzie %s można kupić %s %s za USD po kursie %s i sprzedać na giełdzie %s po kursie %s, zyskując %s."""
                                % (orderBook.siteName, str(orderBook.minAskPrice.quantity), currencyName, str(orderBook.minAskPrice.rate), maxSellPriceOrderBook.siteName, str(maxSellPriceOrderBook.maxBidPrice.rate), str(profit)))
                        return profit
                    elif profit < 0: print("Przez prowizję nie da się zarobić, stracilibyśmy: " + str(profit))
                else: print("Nie można kupić akcji ponieważ portfel nie ma wystarczająco środków, brakujące środki: " + str((askMoney - wallet)))

    return 0



def main():
    wallet = 1000

    while True:
        for currency in currenciesToDownload:
            orderBookBittrex = jsonResponseToOrderBook(orderBookFromAPI(bittrex_url, currency), "bittrex")
            orderBookCex = jsonResponseToOrderBook(orderBookFromAPI(cex_url, currency), "cex")
            orderBookBitstamp = jsonResponseToOrderBook(orderBookFromAPI(bitstamp_url, currency.lower()), "bitstamp")
            orderBookBitbay = jsonResponseToOrderBook(orderBookFromAPI(bitbay_url, currency), "bitbay")
            
            orderBooks = [orderBookBittrex, orderBookCex, orderBookBitstamp, orderBookBitbay]

            wallet += calculateProfit(orderBooks, currency, wallet)
            print("Twój portfel ma wartość: " + str(wallet))

            for orderBook in orderBooks: orderBook = None

        time.sleep(5) # sleep to wait for orderbooks to update



main()