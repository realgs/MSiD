import com.google.gson.Gson
import com.google.gson.annotations.SerializedName

data class chartData(val date: Int, val volume: Double,  @SerializedName("weightedAverage") val average: Double)

object JsonParser{

  fun resolveJson(json: String): Array<chartData>? {
    return Gson().fromJson(json, Array<chartData>::class.java)
  }

}
