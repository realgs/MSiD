import com.google.gson.Gson
import com.google.gson.JsonObject
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


  inline fun < reified T : TickerEntity> getStockBuySell(url: String, stockName: String, entityConstructor: () -> T): BuySell? {

    val tickerEntity : T = entityConstructor()
    val currency = tickerEntity.tickers[3]
    val response = sendRequest(url.replace("{}", currency))
    if(response.statusCode == 200) {
      tickerEntity.receiveJson(response.body)
      return BuySell(stockName, tickerEntity.ask, tickerEntity.bid)
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
  val bittrex = fun(): BuySell? { return fetch.getStockBuySell("https://api.bittrex.com/api/v1.1/public/getticker?market={}", "bittrex", ::BittrexTickerEntity) }
  val bitbay = fun(): BuySell? { return fetch.getStockBuySell("https://bitbay.net/API/Public/{}/ticker.json", "bitbay", ::BitbayTickerEntity) }
  val bitstamp = fun(): BuySell? { return fetch.getStockBuySell("https://www.bitstamp.net/api/v2/ticker/{}", "bitstamp", ::BitStampTickerEntity) }
  val cex = fun(): BuySell? { return fetch.getStockBuySell("https://cex.io/api/ticker/{}", "cex", ::CexTickerEntity) }
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
