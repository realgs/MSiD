import com.google.gson.Gson
import com.google.gson.JsonObject
import com.google.gson.annotations.SerializedName

interface TickerEntity{

  val tickers: Array<String>
  val fee: Double
  val bid : Double
  val ask : Double

}

class BittrexTickerEntity(val res: JsonObject = JsonObject()) : TickerEntity {

  override val tickers = arrayOf<String>("BTC-LTC", "BTC-DOGE", "BTC-POT", "USD-BTC")
  //override val fee: Double = 0.002
  override val fee: Double = 0.0001
  override var bid: Double = 0.1
  override var ask: Double = 0.1

  data class ResultData (
    val Bid: Double,
    val Ask: Double,
    val Last: Double
  )

  init {
    println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(res)
    //if(result != null) {
      val gson = Gson()
      //val res: ResultData = gson.fromJson(result, ResultData::class.java)
      //bid = res.Bid
      //ask = res.Ask
    //}
  }

}

class BitbayTickerEntity(
  @SerializedName("bid")override val bid: Double = 0.0,
  @SerializedName("ask")override val ask: Double = 0.0
) : TickerEntity {

  override val tickers = arrayOf<String>("LTCBTC", "BTCDOGE", "BTCPOT", "BTCUSD")

  //override val fee = 0.0043
  override val fee: Double = 0.0001

}

class BitStampTickerEntity(
  @SerializedName("bid")override val bid: Double = 0.0,
  @SerializedName("ask")override val ask: Double = 0.0
) : TickerEntity {

  override val tickers: Array<String> = arrayOf<String>("ltcbtc", "ethbtc", "bchbtc", "btcusd")
  //override val fee: Double = 0.005
  override val fee: Double = 0.0001

}

class CexTickerEntity(
  @SerializedName("bid")override val bid: Double = 0.0,
  @SerializedName("ask")override val ask: Double = 0.0
) : TickerEntity {

  override val tickers: Array<String> = arrayOf<String>("LTC/BTC", "ETH/BTC", "BCH/BTC", "BTC/USD")
  //override val fee: Double = 0.0025
  override val fee: Double = 0.0001


}
