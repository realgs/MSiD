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


  inline fun < reified T : TickerEntity> getStockBuySell(stockName: String, currency: Int, entityConstructor: () -> T): BuySell? {

    val tickerEntity : T = entityConstructor()
    val currency = tickerEntity.tickers[currency]
    val response = sendRequest(tickerEntity.url.replace("{}", currency))
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
