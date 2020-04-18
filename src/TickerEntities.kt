import com.google.gson.annotations.SerializedName

interface TickerEntity{

  val tickers: Array<String>

  data class MainData (
    val Bid: Double,
    val Ask: Double
  )

}

object BittrexTickerEntity : TickerEntity {

  override val tickers = arrayOf<String>("BTC-LTC", "BTC-DOGE", "BTC-POT", "BTC-USD")

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

  data class MainData(
    @SerializedName("ask")val ask : Double,
    @SerializedName("bid")val bid : Double
  )

}

object CexTickerEntity : TickerEntity {

  override val tickers: Array<String> = arrayOf<String>("LTC/BTC", "ETH/BTC", "BCH/BTC", "BTC/USD")

  data class MainData(
    @SerializedName("ask")val ask : Double,
    @SerializedName("bid")val bid : Double
  )

}
