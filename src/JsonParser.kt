import com.google.gson.Gson
import com.google.gson.annotations.SerializedName

data class ChartData(
  val date: Long,
  val high: Double,
  val low: Double,
  val open: Double,
  val close: Double
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
