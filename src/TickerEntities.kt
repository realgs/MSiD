import com.google.gson.Gson
import com.google.gson.JsonObject
import com.google.gson.annotations.SerializedName
import java.io.Reader

abstract class TickerEntity(){

  abstract val tickers: Array<String>
  abstract val fee: Double
  abstract var bid : Double
  abstract var ask : Double

  open fun receiveJson(json: String){
    val gson = Gson()
    val tickerJson: JsonObject = gson.fromJson(json, JsonObject::class.java)
    bid = tickerJson.get("bid").asDouble
    ask = tickerJson.get("ask").asDouble

  }

}

class BittrexTickerEntity() : TickerEntity() {

  override val tickers = arrayOf<String>("BTC-LTC", "BTC-DOGE", "BTC-POT", "USD-BTC")
  //override val fee: Double = 0.002
  override val fee: Double = 0.0001
  override var bid: Double = 0.0
  override var ask: Double = 0.0

  override fun receiveJson(json: String){
    val gson = Gson()
    val tickerJson: JsonObject = gson.fromJson(json, JsonObject::class.java)

    val resultJson: JsonObject = gson.fromJson(tickerJson.get("result"), JsonObject::class.java)
    println(resultJson)
    bid = resultJson.get("Bid").asDouble
    ask = resultJson.get("Ask").asDouble
  }


}

class BitbayTickerEntity() : TickerEntity() {

  override val tickers = arrayOf<String>("LTCBTC", "BTCDOGE", "BTCPOT", "BTCUSD")

  override val fee = 0.0043
  override var bid: Double = 0.0
  override var ask: Double = 0.0

}

class BitStampTickerEntity() : TickerEntity() {

  override val tickers: Array<String> = arrayOf<String>("ltcbtc", "ethbtc", "bchbtc", "btcusd")
  override val fee: Double = 0.005
  override var bid: Double = 0.0
  override var ask: Double = 0.0

}

class CexTickerEntity() : TickerEntity() {

  override val tickers: Array<String> = arrayOf<String>("LTC/BTC", "ETH/BTC", "BCH/BTC", "BTC/USD")
  override val fee: Double = 0.002
  override var bid: Double = 0.0
  override var ask: Double = 0.0

}
