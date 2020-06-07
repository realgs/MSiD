import requests

CURRENCIES = ['ETH','LTC','TRX','XRP']
FEE = {}
FEE['tokok'] = 0.002
FEE['bitbay'] = 0.001
FEE['latoken'] = 0.001
FEE['biki'] = 0.0015
FEE['hitbtc'] = 0.002

def getBTCtoPLN():
    r = requests.get("https://bitbay.net/API/Public/BTCPLN/orderbook.json")
    return float(r.json()['asks'][0][0])



wallet =1000
outcome = wallet / getBTCtoPLN()

# api data for diffrent markets - since many sites require sign in I've found that in someone else's repo
# tokok = "https://www.tokok.com/api/v1/depth?symbol={}_BTC"
# bitbay = "https://bitbay.net/API/Public/{}BTC/orderbook.json"
# biki = "https://openapi.biki.com/open/api/market_dept?symbol={}btc&type=step0"
# latoken = "https://api.latoken.com/v2/marketOverview/orderbook/{}_BTC"
# hitbtc = ""https://api.hitbtc.com/api/2/public/orderbook/{}BTC.json""
# not working urls
# wave = "https://marketdata.wavesplatform.com/api/v1/"
# bittrex = "https://api.bittrex.com/api/v1.1/public/getorderbook?market=BTC&type=both"



def getMarket(market, URL):
    print("\nRetreiving data from: " + market)
    currentMarket = {}
    for c in CURRENCIES:
        info = {}
        print(c, end =" ")
        respons = requests.get(URL.format(c))
        info['asks'] = respons.json()['asks']
        info['bids'] = respons.json()['bids']
        currentMarket[c] = info
    return currentMarket

def getMarketWithTick(market, URL):
    #Biki market needs "tick" to respond so it have to has own function
    print("\nRetreiving data from: " + market)
    currentMarket = {}
    for c in CURRENCIES:
        info = {}
        print(c, end =" ")
        respons = requests.get(URL.format(c.lower()))
        info['asks'] = respons.json()['data']['tick']['asks']
        info['bids'] = respons.json()['data']['tick']['bids']
        currentMarket[c] = info
    return currentMarket

def calculateOffer(toMe, toMarket, asksOffers, bidsOffers, crypto):
    if (float(asksOffers[0][1]) < float(bidsOffers[0][1])):
        amount = float(asksOffers[0][1])
    else:
        amount = float(bidsOffers[0][1])
    print("Buy {} {} in {} for {}BTC, sell in {} for {}BTC".format(
        amount, crypto, toMe, asksOffers[0][0], toMarket, bidsOffers[0][0]))
    global outcome
    outcome += amount * (float(bidsOffers[0][0]) * (1 + FEE[toMarket]) - float(asksOffers[0][0]) * (1 - FEE[toMe]))
    print("MONEEEEEY = {}BTC".format(outcome))


def bestOfferSearch(market, orderbook):
    for crypto, orders in orderbook.items():
        print("Comparing {} in {} ".format(crypto, market))
        if (orders['asks']):
         bestAskOrder = orders['asks'][0]
         for otherMarketName, otherOrderbook in marketsOrderbooks.items():
            if (otherOrderbook[crypto]['bids']):
                if (float(bestAskOrder[0]) * (1 + FEE[market]) < float(
                        otherOrderbook[crypto]['bids'][0][0]) * (1 - FEE[otherMarketName])):
                    calculateOffer(market, orders['asks'], otherMarketName,
                                   otherOrderbook[crypto]['bids'], crypto)



while (True):
    marketsOrderbooks = {}
    marketsOrderbooks['tokok'] = getMarket("Toktok", "https://www.tokok.com/api/v1/depth?symbol={}_BTC")
    marketsOrderbooks['bitbay'] = getMarket("BitBay", "https://bitbay.net/API/Public/{}BTC/orderbook.json")
    marketsOrderbooks['latoken'] = getMarket("Latoken", "https://api.latoken.com/v2/marketOverview/orderbook/{}_BTC")
    marketsOrderbooks['biki'] = getMarketWithTick("Biki", "https://openapi.biki.com/open/api/market_dept?symbol={}btc&type=step0")

    for market, orderbook in marketsOrderbooks.items():
        print("\n I will now look for best offers in: " + market)
        bestOfferSearch(market, orderbook)
    print("Your overall outcome is astonishing {} PLN".format(outcome * getBTCtoPLN()))
