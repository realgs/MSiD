import time
import requests

def get_data(url):
    response = requests.request("GET", url)
    return response.json()

def getSellsAndBuys(exchange, crypto, website):
    data = get_data(website + crypto)

    if exchange == 'bitbay':
        sellsAndBuys = float(data['ticker']['highestBid']), float(data['ticker']['lowestAsk'])
    if exchange == 'bitfinex':
        sellsAndBuys = data[0], data[2]
    if exchange == 'bittrex':
        sellsAndBuys = data['result']['Bid'], data['result']['Ask']
    if exchange == 'bitstamp':
        sellsAndBuys = float(data['bid']), float(data['ask'])
    return sellsAndBuys

def calculateArbitration(offerToSell, offerToBuy, commission, nameExchangeWithOfferToSell, nameExchangeWithOfferToBuy, myWallet):
    profit = ((offerToBuy) * (1-commission[nameExchangeWithOfferToBuy])) - (offerToSell * (1+commission[nameExchangeWithOfferToSell]))

    if profit > 0:
        myWallet += profit * (myWallet / (offerToSell * (1+commission[nameExchangeWithOfferToSell])))
        return [profit, offerToSell, offerToBuy, nameExchangeWithOfferToSell, nameExchangeWithOfferToBuy], round(myWallet, 2)

    else:
        return False, myWallet

def arbitration(arbitrationDictionary, sellsAndBuys, cryptoTypesInExchange, commission, wallet):
    offersToBuy = 0
    theMostExpensiveToBuy = 0
    nameExchangeWithTheBestOfferToBuy = ""

    offersToSell = 1
    theCheapestToSell = 9999999
    nameExchangeWithTheBestOfferToSell = ""

    for cryptoType in range(len(cryptoTypesInExchange)):

        for exchangeName, data in commission.items():
            if(sellsAndBuys[exchangeName][cryptoType][offersToSell] <= theCheapestToSell):
                theCheapestToSell = sellsAndBuys[exchangeName][cryptoType][offersToSell]
                nameExchangeWithTheBestOfferToSell = exchangeName

            if (sellsAndBuys[exchangeName][cryptoType][offersToBuy] >= theMostExpensiveToBuy):
                theMostExpensiveToBuy = sellsAndBuys[exchangeName][cryptoType][offersToBuy]
                nameExchangeWithTheBestOfferToBuy = exchangeName

        arbitrationDictionary[cryptoTypesInExchange['bitbay'][cryptoType]], wallet = calculateArbitration(theCheapestToSell, theMostExpensiveToBuy, commission, nameExchangeWithTheBestOfferToSell, nameExchangeWithTheBestOfferToBuy, wallet)
        theMostExpensiveToBuy = 0
        theCheapestToSell = 9999999

    return arbitrationDictionary, wallet

def show(types, sellsAndBuys, arbitrationDictionary, wallet):
    print("\n-------------------------------------------------------------------------------------------------------------------------------------")
    for crypto in range(len(types['bitbay'])):
        print("\n" + "Offers for currency: " + types['bitbay'][crypto] + " (buy, sell)")

        for exchange, offersForCurrency in sellsAndBuys.items():
            print(exchange, ":", offersForCurrency[crypto])

        if(arbitrationDictionary[types['bitbay'][crypto]] == False):
            print("<There is no possibility of arbitration>")
        else:
            print("<Most cost-effective arbitration is possible during the purchase: 1[" + types['bitbay'][crypto] + "] for " + str(arbitrationDictionary[types['bitbay'][crypto]][1]) + " in " + arbitrationDictionary[types['bitbay'][crypto]][3] + " and sell for: " + str(arbitrationDictionary[types['bitbay'][crypto]][2]) + " in " + arbitrationDictionary[types['bitbay'][crypto]][4] + ".>")
            print("Profit amount: " + str(arbitrationDictionary[types['bitbay'][crypto]][0]))

    print("\n\n-------------------------------------------------------------------------------------------------------------------------------------")
    print("->My wallet: " + str(wallet) + "$")
    print("->New offers", end="")

    for period in range(5):
        print(".", end="")
        time.sleep(1)

if __name__ == "__main__":
    walletWithDollars = 20000.00
    cryptoTypesInExchange = []
    exchanges = {
        'bitbay': "https://api.bitbay.net/rest/trading/ticker/",
        'bitfinex': "https://api-pub.bitfinex.com/v2/ticker/",
        'bittrex': "https://api.bittrex.com/api/v1.1/public/getticker?market=",
        'bitstamp': "https://www.bitstamp.net/api/v2/ticker/"
    }
    cryptoTypes = {
        'bitbay': ["BTC-USD", "LTC-USD", "ETH-USD", "XRP-USD"],
        'bitfinex': ["tBTCUSD", "tLTCUSD", "tETHUSD", "tXRPUSD"],
        'bittrex': ["USD-BTC", "USD-LTC", "USD-ETH", "USD-XRP"],
        'bitstamp': ["btcusd", "ltcusd", "ethusd", "xrpusd"]
    }
    sellsAndBuysForCryptoTypes = {
        'bitbay': [],
        'bitfinex': [],
        'bittrex': [],
        'bitstamp': []
    }
    arbitrationForCryptoTypes = {
        'BTC-USD': [],
        'LTC-USD': [],
        'ETH-USD': [],
        'XRP-USD': []
    }
    commission = {
        'bitbay': 0.001,
        'bitfinex': 0.002,
        'bittrex': 0.002,
        'bitstamp': 0.005
    }

    while(True):

        for exchangeName, url in exchanges.items():                                                                     #get: exchangeName, url and cryptoTypesInExchange
            cryptoTypesInExchange = cryptoTypes[exchangeName]

            for cryptoType in cryptoTypesInExchange:                                                                    #set offers (sellsAndBuysForCryptoTypes for every exchangeName) to matrix
                sellsAndBuysForCryptoTypes[exchangeName].append(getSellsAndBuys(exchangeName, cryptoType, url))

        arbitrationForCryptoTypes, walletWithDollars = arbitration(arbitrationForCryptoTypes, sellsAndBuysForCryptoTypes, cryptoTypes, commission, walletWithDollars)

        show(cryptoTypes, sellsAndBuysForCryptoTypes, arbitrationForCryptoTypes, walletWithDollars)                     #show filled matrix and prepare matrix for new data
        for exchange, data in sellsAndBuysForCryptoTypes.items():
            sellsAndBuysForCryptoTypes[exchange] = []
