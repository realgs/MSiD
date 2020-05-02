from fetcher import MarketInfo

def findLowHigh(fetchedInfo):
    fetchedInfo.buyForLowest = fetchedInfo.asks[0]
    fetchedInfo.sellForHighest = fetchedInfo.bids[len(fetchedInfo.bids)-1]
    return fetchedInfo

def findLowHighAll(fetchedData):
    output = []
    for d in fetchedData:
        output.append(findLowHigh(d))
    return output

def canBeProfitable(marketToBuyFrom, marketToSellTo):
    buyFor =  marketToBuyFrom.buyForLowest
    sellFor = marketToSellTo.sellForHighest
    return buyFor[1] < sellFor[1]

def calculateTrade(marketToBuyFrom, marketToSellTo):
    currency = marketToBuyFrom.currency.split("-")
    buyFor =  marketToBuyFrom.buyForLowest
    sellFor = marketToSellTo.sellForHighest
    amount = min(buyFor[0], sellFor[0])
    buyingPrice = amount * buyFor[1]
    sellingPrice = (amount - amount * marketToBuyFrom.takerFee) * sellFor[1]
    profit = sellingPrice - buyingPrice
    print(f"At {marketToBuyFrom.market:8} you can buy {amount:8.5f} {currency[1]} at rate {buyFor[1]:8.5f} {currency[0]} and sell at {marketToSellTo.market:8} at rate {sellFor[1]:8.5f} {currency[0]} for {profit:.2f} {currency[0]} profit (including {amount * marketToBuyFrom.takerFee *sellFor[1]:.2f} {currency[0]} fee).")
    return profit
