import com.google.gson.Gson
import kotlinx.coroutines.delay
import kotlinx.coroutines.runBlocking
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

  val getBittrexBuySell = fun(): BuySell {
    val currency = BittrexTickerEntity.tickers[3]
    val response = sendRequest("https://api.bittrex.com/api/v1.1/public/getticker?market=$currency")
    val gson = Gson()
    val ticker: BittrexTickerEntity.MainData = gson.fromJson(response.body, BittrexTickerEntity.MainData::class.java)
    if(ticker.success) {
      println(currency)
      val buyVal = ticker.result.Ask + ticker.result.Ask * BittrexTickerEntity.fee
      val sellVal = ticker.result.Bid - ticker.result.Bid * BittrexTickerEntity.fee
      return BuySell("bittrex", buyVal, sellVal)
    }

    println("Could not receive data about $currency")
    return BuySell("bittrex")

  }

  val getBitBayBuySell = fun(): BuySell {

    val currency = BitbayTickerEntity.tickers[3]
    val response = sendRequest("https://bitbay.net/API/Public/$currency/ticker.json")
    val gson = Gson()
    val ticker: BitbayTickerEntity.MainData = gson.fromJson(response.body, BitbayTickerEntity.MainData::class.java)
    val buyVal = ticker.ask + ticker.ask * BitbayTickerEntity.fee
    val sellVal = ticker.bid - ticker.bid * BitbayTickerEntity.fee
    return BuySell("bitbay", buyVal, sellVal)

  }

  val getBitStampBuySell= fun(): BuySell {

    val currency = BitStampTickerEntity.tickers[3]
    val response = sendRequest("https://www.bitstamp.net/api/v2/ticker/$currency")
    val gson = Gson()
    val ticker: BitStampTickerEntity.MainData = gson.fromJson(response.body, BitStampTickerEntity.MainData::class.java)
    val buyVal = ticker.ask + ticker.ask * BitStampTickerEntity.fee
    val sellVal = ticker.bid - ticker.bid * BitStampTickerEntity.fee
    return BuySell("bitstamp", buyVal, sellVal)

  }

  val getCexBuySell = fun(): BuySell {

    val currency = CexTickerEntity.tickers[3]
    val response = sendRequest("https://cex.io/api/ticker/$currency")
    val gson = Gson()
    val ticker: CexTickerEntity.MainData = gson.fromJson(response.body, CexTickerEntity.MainData::class.java)
    val buyVal = ticker.ask + ticker.ask * CexTickerEntity.fee
    val sellVal = ticker.bid - ticker.bid * CexTickerEntity.fee
    return BuySell("cex", buyVal, sellVal)

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
  val currencyPair = Pair("USD", "BTC")
  val allStocks: List<() -> BuySell> = listOf(fetch.getBittrexBuySell, fetch.getBitBayBuySell, fetch.getBitStampBuySell, fetch.getCexBuySell)

  runBlocking {

    while(true) {
      val stockResults = StockOperations.watchAllStocks(allStocks)
      StockOperations.checkMarkets(stockResults, currencyPair)
      delay(5000)
    }
  }

  while(true){
    Thread.sleep(5000)
  }

}
