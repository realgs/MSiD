import com.example.stockapp.BuySell
import com.example.stockapp.Response
import java.net.HttpURLConnection
import java.net.URL

object FetchApi {
  fun sendRequest(url: String): Response {
    val conn = URL(url).openConnection() as HttpURLConnection

    with(conn) {
      requestMethod = "GET"
    }

    val responseBody = conn.inputStream.use { it.readBytes() }.toString(Charsets.UTF_8)

    return Response(conn.responseCode, responseBody)
  }


  inline fun < reified T : TickerEntity> getStockBuySell(stockName: String, currency: Int, buyCur: String, sellCur: String, entityConstructor: () -> T): BuySell? {
    val tickerEntity : T = entityConstructor()
    val currency = tickerEntity.tickers[currency]
    val response = sendRequest(tickerEntity.url.replace("{}", currency))
    return if(response.statusCode == 200) {
      tickerEntity.receiveJson(response.body)
      BuySell(stockName, tickerEntity.fee, tickerEntity.ask, tickerEntity.bid, buyCur, sellCur)
    }
    else{
      println("Failed to receive data from $stockName market!")
      return null
    }
  }

}
