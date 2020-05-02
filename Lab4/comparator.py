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
    #print(f"Buy {buyFor[0]} for: {buyFor[1]:.8f} | Sell {sellFor[0]} for: {sellFor[1]:.8f}")
    return buyFor[1] < sellFor[1]

def calculateTrade(marketToBuyFrom, marketToSellTo):
    buyFor =  marketToBuyFrom.buyForLowest
    sellFor = marketToSellTo.sellForHighest
    amount = min(buyFor[0], sellFor[0])
    buyingPrice = amount * buyFor[1]
    sellingPrice = amount * sellFor[1]
    profit = sellingPrice - buyingPrice
    print(f"You can buy {amount:.8f} {marketToBuyFrom.currency} for {buyingPrice:.8f} from {marketToBuyFrom.market} and sell for {sellingPrice:.8f} at {marketToSellTo.market} with profit of {profit:.8f}$")
    return profit
