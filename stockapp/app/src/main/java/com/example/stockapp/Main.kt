import kotlinx.coroutines.delay
import kotlinx.coroutines.runBlocking

fun arbitrage(currencyPair: Pair<String, String>){

  val wallet = Wallet(10000.0, currencyPair.first, currencyPair.second )
  val bittrex = fun(): BuySell? { return FetchApi.getStockBuySell("bittrex", 3, ::BittrexTickerEntity) }
  val bitbay = fun(): BuySell? { return FetchApi.getStockBuySell("bitbay", 3, ::BitbayTickerEntity) }
  val bitstamp = fun(): BuySell? { return FetchApi.getStockBuySell("bitstamp", 3, ::BitStampTickerEntity) }
  val cex = fun(): BuySell? { return FetchApi.getStockBuySell("cex", 3, ::CexTickerEntity) }
  val allStocks: List<() -> BuySell?> = listOf(bittrex, bitbay, bitstamp, cex)

  runBlocking {

    while(true) {
      val stockResults = StockOperations.watchAllStocks(allStocks)
      val profitPair = StockOperations.checkMarkets(stockResults, currencyPair)
      if(profitPair != null) {
        wallet.transStockTransaction(profitPair.first, profitPair.second)
      }
      delay(5000)
    }
  }

  while(true){
    Thread.sleep(5000)
  }

}


fun ex4(stockResult: BuySell?, wallet: Wallet): Boolean {
  if(stockResult != null) {
    val realSellVal = stockResult.sell - (stockResult.sell * stockResult.fee)
    val realBuyVal = stockResult.buy + (stockResult.buy * stockResult.fee)
    StockOperations.printMarket(stockResult, realBuyVal, realSellVal)
//    chartCanvas.updateChart(realSellVal, realBuyVal)
    val decisionMade = DecisionAgent.makeDecision(realSellVal, realBuyVal) //if true -> buy, if false -> sell, if null -> do nothing
    if(decisionMade != null) {
      if (decisionMade) {
        wallet.buy(stockResult.buy, stockResult.fee)
      } else {
        wallet.sell(stockResult.sell, stockResult.fee)
      }
      return true
    }
  }
  return false
}

fun realTimeEx4(){

  val currencyPair = Pair("USD", "BSV")
  val bittrex = fun(): BuySell? { return FetchApi.getStockBuySell("bittrex", 4,  ::BittrexTickerEntity) }
  val wallet = Wallet(1000.0, currencyPair.first, currencyPair.second)

  runBlocking {

    while(true) {
      val stockResult = StockOperations.watchStock(bittrex)
      ex4(stockResult, wallet)
      delay(5000)
    }

  }

  while(true){
    Thread.sleep(5000)
  }

}

fun main(){
  //ex1_3()
  realTimeEx4()
}
