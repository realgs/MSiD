import kotlinx.coroutines.*

object StockOperations{

  fun getPercantageDiff(buy: Double, sell: Double) : Double{
    return 1 - (sell - buy) / sell
  }

  suspend fun watchStock(methodToExecute : () -> BuySell?): BuySell? {
      val awaitedMethod = GlobalScope.async {
        methodToExecute()
      }
      return awaitedMethod.await()
  }

  suspend fun watchAllStocks(methodsToExecute: List<() -> BuySell?>): List<BuySell?> {

    val deferred = methodsToExecute.map { stock ->
      GlobalScope.async {
        stock()
      }
    }

    return deferred.map { it.await() }

  }

  fun printMarket(stock: BuySell?){
    if(stock != null) {
      println("Name: ${stock.stockName}")
      println("Buy: ${stock.buy} Sell: ${stock.sell}\n")
      println("percantageDiff: ${StockOperations.getPercantageDiff(stock.buy, stock.sell)}\n")
    }
  }

  fun checkMarkets(stockResults: List<BuySell?>, currencyPair: Pair<String?, String?>): Pair<BuySell?, BuySell?>? {
    var lowestBuy = Double.MAX_VALUE
    var highestSell = 0.0
    var stockToBuyOn: BuySell? = null
    var stockToSellOn: BuySell? = null
    for (stock in stockResults) {
      if(stock != null) {
        printMarket(stock)
        val realStockBuyVal = stock.buy + (stock.buy * stock.fee)
        if (realStockBuyVal < lowestBuy) {
          lowestBuy = realStockBuyVal
          stockToBuyOn = stock
        }
        val realStockSellVal = stock.sell - (stock.sell * stock.fee)
        if (realStockSellVal > highestSell) {
          highestSell = realStockSellVal
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


