import com.google.gson.Gson
import kotlinx.coroutines.delay
import kotlinx.coroutines.runBlocking
import java.net.HttpURLConnection
import java.net.URL

data class Response(val statusCode: Int, val body: String)
data class BuySell( val stockName: String, val buy: Double = 0.0, val sell: Double = 0.0)

class FetchApi() {
  fun sendRequest(url: String): Response {
    val conn = URL(url).openConnection() as HttpURLConnection

    with(conn) {
      requestMethod = "GET"
    }

    val responseBody = conn.inputStream.use { it.readBytes() }.toString(Charsets.UTF_8)

    return Response(conn.responseCode, responseBody)
  }


  inline fun < reified T : TickerEntity> getStockBuySell(url: String, stockName: String): BuySell? {

    val tickerEntity : T = T::class.java.getConstructor().newInstance()
    //println(tickerEntity)
    val currency = tickerEntity.tickers[3]
    val response = sendRequest(url.replace("{}", currency))
    if(response.statusCode == 200) {
      val gson = Gson()
      //println(response.body)
      val ticker: T = gson.fromJson(response.body, T::class.java)
      return BuySell(stockName, ticker.ask, ticker.bid)
    }
    else{
      println("Failed to receive data from $stockName market!")
      return null
    }
  }



}

fun main(){

  val fetch: FetchApi = FetchApi()
  val currencyPair = Pair("USD", "BTC")
  val wallet = Wallet(10000.0, currencyPair.first, currencyPair.second )
  val bittrex = fun(): BuySell? { return fetch.getStockBuySell<BittrexTickerEntity>("https://api.bittrex.com/api/v1.1/public/getticker?market={}", "bittrex") }
  val bitbay = fun(): BuySell? { return fetch.getStockBuySell<BitbayTickerEntity>("https://bitbay.net/API/Public/{}/ticker.json", "bitbay") }
  val bitstamp = fun(): BuySell? { return fetch.getStockBuySell<BitStampTickerEntity>("https://www.bitstamp.net/api/v2/ticker/{}", "bitstamp") }
  val cex = fun(): BuySell? { return fetch.getStockBuySell<CexTickerEntity>("https://cex.io/api/ticker/{}", "cex") }
  val allStocks: List<() -> BuySell?> = listOf(bitbay, bitstamp, cex)

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

//  data class bitt(val result: String) {
//    val someVal: String = "string"
//    fun method() {
//      print("something")
//    }
//  }
//
//  val response = fetch.sendRequest("https://api.bittrex.com/api/v1.1/public/getticker?market=USD-BTC")
//  println(response)
//  val gson = Gson()
//  val ticker = gson.fromJson(response.body, bitt::class.java)
//  println(ticker)

}
