import java.net.HttpURLConnection
import java.net.URL

object ApiFetch {

  fun sendRequest(url: String): String {
    val conn = URL(url).openConnection() as HttpURLConnection

    with(conn) {
      requestMethod = "GET"
    }

    val responseBody = conn.inputStream.use { it.readBytes() }.toString(Charsets.UTF_8)

    return responseBody

  }

}
