import com.google.gson.Gson

data class ChartData(
  val high: Double,
  val low: Double,
  val open: Double,
  val close: Double,
  val volume: Double
)

object JsonParser{

  fun resolveJson(json: String): List<ChartData>? {
    try{
      return Gson().fromJson(json, Array<ChartData>::class.java).toList()
    }
    catch(e: Exception){
      println(json)
    }
    return null
  }

}
