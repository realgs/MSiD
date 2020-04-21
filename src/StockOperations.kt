import kotlinx.coroutines.*

object StockOperations{

  fun getPercantageDiff(buySell: BuySell) : Double{
    return 1 - (buySell.sell - buySell.buy) / buySell.buy
  }

  fun watchStock(methodToExecute : () -> BuySell): BuySell {
      return methodToExecute()
  }

  suspend fun watchAllStocks(methodsToExecute: List<() -> BuySell?>): List<BuySell?> {

    val deferred = methodsToExecute.map { stock ->
      GlobalScope.async {
        stock()
      }
    }

    return deferred.map { it.await() }

  }

  fun checkMarkets(stockResults: List<BuySell?>, currencyPair: Pair<String?, String?>): Pair<BuySell?, BuySell?>? {
    var lowestBuy = Double.MAX_VALUE
    var highestSell = 0.0
    var stockToBuyOn: BuySell? = null
    var stockToSellOn: BuySell? = null
    for (stock in stockResults) {
      if(stock != null) {
        println("Name: ${stock.stockName}")
        println("Buy: ${stock.buy} Sell: ${stock.sell}")
        println("percantageDiff: ${StockOperations.getPercantageDiff(stock)}\n")
        if (stock.buy < lowestBuy) {
          lowestBuy = stock.buy
          stockToBuyOn = stock
        }
        if (stock.sell > highestSell) {
          highestSell = stock.sell
          stockToSellOn = stock
        }
      }
    }

    if(stockToBuyOn != null && stockToSellOn != null){
      if(lowestBuy < highestSell){
        val profit = Math.round((highestSell - lowestBuy) * 100.00) / 100.00
        println("You might make $profit ${currencyPair.first} if you buy 1 ${currencyPair.second} for $lowestBuy ${currencyPair.first} on ${stockToBuyOn.stockName} " +
          "and sell it for $highestSell ${currencyPair.first} on ${stockToSellOn.stockName}\n")
        return Pair<BuySell, BuySell>(stockToBuyOn, stockToSellOn)
      }
      else println("Noting to profit on\n")
    }
    return null
  }

}


