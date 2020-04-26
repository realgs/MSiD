import kotlinx.coroutines.delay
import kotlinx.coroutines.runBlocking
import java.util.*

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
        wallet.transaction(profitPair.first, profitPair.second)
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
        DBHelper.insertData(stockResult)
      }
      delay(freq)
    }
  }

  while(true){
    Thread.sleep(freq)
  }
}

fun ex4(){

//TODO: get predicted value of price using linear regression and compare to actual value. Dynamically change predicted value based on last x measurements

}

fun main(){
  ex4()
}
