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

def calculateTrade(marketToBuyFrom, marketToSellTo, budget):
    buyFor =  marketToBuyFrom.buyForLowest
    sellFor = marketToSellTo.sellForHighest
    amount = min(buyFor[0], sellFor[0])
    if amount * buyFor[1] > budget:
        amount = budget/buyFor[1]
    buyingPrice = amount * buyFor[1]
    sellingPrice = (amount - amount * marketToBuyFrom.takerFee) * sellFor[1]
    profit = sellingPrice - buyingPrice
    return [amount, profit]
