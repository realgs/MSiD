import java.lang.Exception
import java.time.LocalDateTime
import java.time.ZoneId
import java.time.format.DateTimeFormatter

fun main() {

  print("Enter valid currency pair (e.g. BTC_ETH): ")
  val currencyPair = readLine()

  println("Format of datetime is yyyy-mm-ddThh:mm:ss")
  print("Enter start date: ")

  try {
    val startDate = LocalDateTime.parse(readLine(), DateTimeFormatter.ISO_LOCAL_DATE_TIME).atZone(ZoneId.of("UTC")).toEpochSecond()

    print("Enter end date: ")
    val endDate = LocalDateTime.parse(readLine(), DateTimeFormatter.ISO_LOCAL_DATE_TIME).atZone(ZoneId.of("UTC")).toEpochSecond()


    if(startDate > endDate){
      println("End date happens earlier than start date")
      return
    }

    val mapOfIntervals = arrayListOf<Int>(300, 900, 1800, 7200, 14400, 86400)

    print("Select interval:\n" +
      "1. 5 minutes\n" +
      "2. 15 minutes\n" +
      "3. 30 minutes\n" +
      "4. 2 hours\n" +
      "5. 4 hours\n" +
      "6. 24 hours\n")

    var selectedInterval: String? = null

    while (selectedInterval == null){
      selectedInterval = readLine()
      if (selectedInterval != null) {
        if (selectedInterval.toInt() in 1..6) {
          val interval = mapOfIntervals[selectedInterval.toInt() - 1]
          val result = ApiFetch.sendRequest("https://poloniex.com/public?command=returnChartData&currencyPair=$currencyPair&start=$startDate&end=$endDate&period=$interval")
          val parsed = JsonParser.resolveJson(result)
          if (parsed != null) {
            ChartCanvas("Wykres!", parsed)
            val generated = Simulator(parsed).simulate(endDate + interval, interval).toList()
            ChartCanvas("Wygenerowane!", generated)
          }
        } else {
          println("Select valid interval")
          selectedInterval = null
        }
      }
    }

  }
  catch(e: Exception){
    e.printStackTrace()
  }

}
