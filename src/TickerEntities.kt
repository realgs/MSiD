import com.google.gson.annotations.SerializedName

interface TickerEntity{

  val tickers: Array<String>
  val fee: Double

  data class MainData (
    val Bid: Double,
    val Ask: Double
  )

}

object BittrexTickerEntity : TickerEntity {

  override val tickers = arrayOf<String>("BTC-LTC", "BTC-DOGE", "BTC-POT", "USD-BTC")
  //override val fee: Double = 0.002
  override val fee: Double = 0.0001

  data class MainData(
    val success: Boolean,
    val message: String,
    val result: ResultData
  )

  data class ResultData (
    val Bid: Double,
    val Ask: Double,
    val Last: Double
  )

}

object BitbayTickerEntity : TickerEntity {

  override val tickers = arrayOf<String>("LTCBTC", "BTCDOGE", "BTCPOT", "BTCUSD")

  //override val fee = 0.0043
  override val fee: Double = 0.0001

  data class MainData(
    val max : Double,
    val min : Double,
    val last : Double,
    val bid : Double,
    val ask : Double,
    val vwap : Double,
    val average : Double,
    val volume : Double
  )

}

object BitStampTickerEntity : TickerEntity {

  override val tickers: Array<String> = arrayOf<String>("ltcbtc", "ethbtc", "bchbtc", "btcusd")
  //override val fee: Double = 0.005
  override val fee: Double = 0.0001

  data class MainData(
    @SerializedName("ask")val ask : Double,
    @SerializedName("bid")val bid : Double
  )

}

object CexTickerEntity : TickerEntity {

  override val tickers: Array<String> = arrayOf<String>("LTC/BTC", "ETH/BTC", "BCH/BTC", "BTC/USD")
  //override val fee: Double = 0.0025
  override val fee: Double = 0.0001

  data class MainData(
    @SerializedName("ask")val ask : Double,
    @SerializedName("bid")val bid : Double
  )

}
