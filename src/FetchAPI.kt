import com.google.gson.Gson
import java.net.HttpURLConnection
import java.net.URL

data class Response(val statusCode: Int, val body: String)
data class BuySell(val buy: Double = 0.0, val sell: Double = 0.0)

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
    val currency = BittrexTickerEntity.tickers[0]
    val response = sendRequest("https://api.bittrex.com/api/v1.1/public/getticker?market=$currency")
    val gson = Gson()
    val ticker: BittrexTickerEntity.MainData = gson.fromJson(response.body, BittrexTickerEntity.MainData::class.java)
    if(ticker.success) {
      println(currency)
      return BuySell(ticker.result.Ask, ticker.result.Bid)
    }

    println("Could not receive data about $currency")
    return BuySell()

  }
}

suspend fun main(){
  val fetch: FetchApi = FetchApi()
  StockOperations.watchStock(5000, fetch.getBittrexBuySell)
}
