import com.google.gson.Gson
import com.google.gson.JsonObject

abstract class TickerEntity(){

  abstract val tickers: Array<String>
  abstract val fee: Double
  abstract val url: String
  open var bid : Double = 0.0
  open var ask : Double = 0.0

  open fun receiveJson(json: String){
    val gson = Gson()
    val tickerJson: JsonObject = gson.fromJson(json, JsonObject::class.java)
    bid = tickerJson.get("bid").asDouble
    ask = tickerJson.get("ask").asDouble

  }

}

class BittrexTickerEntity() : TickerEntity() {

  override val tickers = arrayOf<String>("BTC-LTC", "USD-BTC", "USD-LTC")
  override val url: String = "https://api.bittrex.com/api/v1.1/public/getticker?market={}"
  override val fee: Double = 0.002

  override fun receiveJson(json: String){
    val gson = Gson()
    val tickerJson: JsonObject = gson.fromJson(json, JsonObject::class.java)
    val resultJson: JsonObject = gson.fromJson(tickerJson.get("result"), JsonObject::class.java)
    bid = resultJson.get("Bid").asDouble
    ask = resultJson.get("Ask").asDouble
  }


}

class BitbayTickerEntity() : TickerEntity() {

  override val tickers = arrayOf<String>("LTCBTC", "BTCUSD", "LTCUSD")
  override val url: String = "https://bitbay.net/API/Public/{}/ticker.json"
  override val fee = 0.0043

}

class BitStampTickerEntity() : TickerEntity() {

  override val tickers: Array<String> = arrayOf<String>("ltcbtc", "btcusd","ltcusd")
  override val url: String = "https://www.bitstamp.net/api/v2/ticker/{}"
  override val fee: Double = 0.005

}

class CexTickerEntity() : TickerEntity() {

  override val tickers: Array<String> = arrayOf<String>("LTC/BTC", "BTC/USD", "LTC/USD")
  override val url: String = "https://cex.io/api/ticker/{}"
  override val fee: Double = 0.002

}
