open class TickerEntity{}

object BittrexTickerEntity : TickerEntity() {

  val tickers = arrayOf<String>("BTC-LTC", "BTC-DOGE", "BTC-POT", "BTC-USD")

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

object BitbayTickerEntity : TickerEntity() {

  val tickers = arrayOf<String>("LTCBTC", "BTCDOGE", "BTCPOT", "BTCUSD")

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
