import kotlinx.coroutines.delay
import kotlinx.coroutines.runBlocking
import kotlin.collections.ArrayList

fun ex1_3(){

  val fetch: FetchApi = FetchApi()
  val currencyPair = Pair("USD", "BTC")
  val wallet = Wallet(10000.0, currencyPair.first, currencyPair.second )
  val bittrex = fun(): BuySell? { return fetch.getStockBuySell("bittrex", 3, ::BittrexTickerEntity) }
  val bitbay = fun(): BuySell? { return fetch.getStockBuySell("bitbay", 3, ::BitbayTickerEntity) }
  val bitstamp = fun(): BuySell? { return fetch.getStockBuySell("bitstamp", 3, ::BitStampTickerEntity) }
  val cex = fun(): BuySell? { return fetch.getStockBuySell("cex", 3, ::CexTickerEntity) }
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

fun collectData(freq:Long = 5000){
  val fetch: FetchApi = FetchApi()
  val bittrex = fun(): BuySell? { return fetch.getStockBuySell("bittrex", 4,  ::BittrexTickerEntity) }

  runBlocking {

    while(true) {
      val stockResult = StockOperations.watchStock(bittrex)
      if(stockResult != null) {
        StockOperations.printMarket(stockResult)
        chartCanvas.updateChart(stockResult.sell, stockResult.buy)
      }
      delay(freq)
    }
  }

  while(true){
    Thread.sleep(freq)
  }
}

fun getSublist(from:List<BuySell>?, offset:Int = 0, size:Int = 1): Pair<MutableList<Double>, MutableList<Double>> {
  val allSell: MutableList<Double> = ArrayList<Double>()
  val allBuy: MutableList<Double> = ArrayList<Double>()
  val pieceOfList = from?.subList(offset, offset + size)
  for(data in pieceOfList!!) {
    allSell.add(data.sell)
    allBuy.add(data.buy)
  }
  return Pair(allBuy, allSell)
}

fun ex4(){

  val currencyPair = Pair("USD", "BSV")
  val fetch: FetchApi = FetchApi()
  val bittrex = fun(): BuySell? { return fetch.getStockBuySell("bittrex", 4,  ::BittrexTickerEntity) }
  val wallet = Wallet(1000.0, currencyPair.first, currencyPair.second)

  runBlocking {

    while(true) {
      val stockResult = StockOperations.watchStock(bittrex)
      if(stockResult != null) {
        StockOperations.printMarket(stockResult)
        chartCanvas.updateChart(stockResult.sell, stockResult.buy)
        val decisionMade = DecisionAgent.makeDecision(stockResult.sell, stockResult.buy)
        if(decisionMade != null) {
          if (decisionMade) {
            wallet.buy(stockResult.buy)
          } else {
            wallet.sell(stockResult.sell)
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

    results?.forEach { it ->
      StockOperations.printMarket(it)
      chartCanvas.updateChart(it.sell, it.buy)
      val decisionMade = DecisionAgent.makeDecision(it.sell, it.buy)
      if (decisionMade != null) {
        if (decisionMade) {
          wallet.buy(it.buy)
        } else {
          wallet.sell(it.sell)
        }
        Thread.sleep(5000)
      }
      Thread.sleep(100)
    }

}

fun main(){
  ex1_3()
}
