import kotlinx.coroutines.delay
import kotlinx.coroutines.runBlocking
import kotlin.collections.ArrayList

fun ex1_3(){

  val currencyPair = Pair("USD", "BTC")
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

fun ex4(){

  val currencyPair = Pair("USD", "BSV")
  val bittrex = fun(): BuySell? { return FetchApi.getStockBuySell("bittrex", 4,  ::BittrexTickerEntity) }
  val wallet = Wallet(1000.0, currencyPair.first, currencyPair.second)
  val fee = BittrexTickerEntity().fee

  runBlocking {

    while(true) {
      val stockResult = StockOperations.watchStock(bittrex)
      if(stockResult != null) {
        val newSellVal = stockResult.sell - (stockResult.sell * fee)
        val newBuyVal = stockResult.buy + (stockResult.buy * fee)
        StockOperations.printMarket(BuySell(stockResult.stockName, stockResult.fee, newSellVal, newBuyVal))
        //DBHelper.insertData(stockResult)
        val decisionMade = DecisionAgent.makeDecision(newSellVal, newBuyVal)
        chartCanvas.updateChart(newSellVal, newBuyVal)
        if(decisionMade != null) {
          if (decisionMade) {
            wallet.buy(stockResult.buy, stockResult.fee)
          } else {
            wallet.sell(stockResult.sell, stockResult.fee)
          }
        }
      }
      delay(5000)
    }
  }

  while(true){
    Thread.sleep(5000)
  }

}

fun simulation(){
  val currencyPair = Pair("USD", "BSV")
  val wallet = Wallet(1000.0, currencyPair.first, currencyPair.second)
  val results = DBHelper.selectBuySell()
  val fee = BittrexTickerEntity().fee

    results?.forEach { it ->
      val newSellVal = it.sell - (it.sell * fee)
      val newBuyVal = it.buy + (it.buy * fee)
      StockOperations.printMarket(BuySell(it.stockName, it.fee, newBuyVal, newSellVal))
      chartCanvas.updateChart(newSellVal, newBuyVal)
      val decisionMade = DecisionAgent.makeDecision(newSellVal, newBuyVal)
      if (decisionMade != null) {
        if (decisionMade) {
          wallet.buy(it.buy, fee)
        } else {
          wallet.sell(it.sell, fee)
        }
        Thread.sleep(5000)
      }
      Thread.sleep(100)
    }

  println(wallet.totalProfit)

}

fun main(){
  simulation()
}
