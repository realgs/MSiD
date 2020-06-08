object BittrexTickerEntity {

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
