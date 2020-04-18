import com.google.gson.Gson
import kotlinx.coroutines.*
import java.net.HttpURLConnection
import java.net.URL

data class Response(val statusCode: Int, val body: String)
data class BuySell( val stockName: String, val buy: Double = 0.0, val sell: Double = 0.0)

class FetchApi() {
  private fun sendRequest(url: String): Response {
    val conn = URL(url).openConnection() as HttpURLConnection

    with(conn) {
      requestMethod = "GET"
    }

    val responseBody = conn.inputStream.use { it.readBytes() }.toString(Charsets.UTF_8)

    return Response(conn.responseCode, responseBody)
  }

  fun getBittrexBuySell(): () -> BuySell {
    val currency = BittrexTickerEntity.tickers[0]
    val response = sendRequest("https://api.bittrex.com/api/v1.1/public/getticker?market=$currency")
    val gson = Gson()
    val ticker: BittrexTickerEntity.MainData = gson.fromJson(response.body, BittrexTickerEntity.MainData::class.java)
    if(ticker.success) {
      println(currency)
      return { BuySell("bittrex", ticker.result.Ask, ticker.result.Bid) }
    }

    println("Could not receive data about $currency")
    return { BuySell("bittrex") }

  }

  fun getBitBayBuySell(): () -> BuySell {

    val currency = BitbayTickerEntity.tickers[0]
    val response = sendRequest("https://bitbay.net/API/Public/$currency/ticker.json")
    val gson = Gson()
    val ticker: BitbayTickerEntity.MainData = gson.fromJson(response.body, BitbayTickerEntity.MainData::class.java)
    return { BuySell("bitbay", ticker.ask, ticker.bid) }

  }

  fun getBitStampBuySell(): () -> BuySell {

    val currency = BitStampTickerEntity.tickers[0]
    val response = sendRequest("https://www.bitstamp.net/api/v2/ticker/$currency")
    val gson = Gson()
    val ticker: BitStampTickerEntity.MainData = gson.fromJson(response.body, BitStampTickerEntity.MainData::class.java)
    return { BuySell("bitstamp", ticker.ask, ticker.bid) }

  }

  fun getCexBuySell(): () -> BuySell {

    val currency = CexTickerEntity.tickers[0]
    val response = sendRequest("https://cex.io/api/ticker/$currency")
    val gson = Gson()
    val ticker: CexTickerEntity.MainData = gson.fromJson(response.body, CexTickerEntity.MainData::class.java)
    return { BuySell("cex", ticker.ask, ticker.bid) }

  }

//  fun <T : TickerEntity> getStockBuySell(url: String, stockName: String): () -> BuySell {
//
//    val tickerEntity : T = T
//    val currency = tickerEntity.tickers[0]
//    val response = sendRequest(url.replace("{}", currency))
//    val gson = Gson()
//    val ticker: tickerEntity.MainData = gson.fromJson(response.body, tickerEntity.MainData::class.java)
//    println(currency)
//    return { BuySell (stockName, ticker.Ask, ticker.Bid) }
//  }
}

suspend fun main(){

  val fetch: FetchApi = FetchApi()

  val allStocks: List<() -> BuySell> = listOf(fetch.getBittrexBuySell(), fetch.getBitBayBuySell(), fetch.getBitStampBuySell(), fetch.getCexBuySell())

  runBlocking {

    while(true) {
      val stockResults = StockOperations.watchAllStocks(allStocks)
      for (stock in stockResults) {
        println("Name: ${stock.stockName}")
        println("Buy: ${stock.buy} Sell: ${stock.sell}")
        println("percantageDiff: ${StockOperations.getPercantageDiff(stock)}\n")
      }
      delay(5000)
    }
  }

  while(true){
    Thread.sleep(5000)
  }

}
