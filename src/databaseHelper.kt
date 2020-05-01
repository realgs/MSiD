import java.sql.*
import java.util.*

object DBHelper{
  const val DRIVER = "org.sqlite.JDBC"
  const val DB_URL = "jdbc:sqlite:buySell.db"
  private val conn: Connection
  private val stat: Statement

  init {
    Class.forName("org.sqlite.JDBC");
    conn = DriverManager.getConnection(DB_URL)
    stat = conn.createStatement()
  }

  fun createTable(){
    val createTable =
      "CREATE TABLE IF NOT EXISTS buySellData (stockName text, buy double, sell double)"
    try {
      stat.execute(createTable)
    } catch (e: SQLException) {
      System.err.println("Couldn't create table")
      e.printStackTrace()
    }
  }

  fun insertData(buySell: BuySell): Boolean {
    try {
      val prepStmt: PreparedStatement = conn.prepareStatement(
        "INSERT INTO buySellData VALUES (?, ?, ?);"
      )
      prepStmt.setString(1, buySell.stockName)
      prepStmt.setDouble(2, buySell.buy)
      prepStmt.setDouble(3, buySell.sell)
      prepStmt.execute()
    } catch (e: SQLException) {
      System.err.println("Couldn't insert data")
      e.printStackTrace()
      return false
    }
    return true
  }

  fun selectBuySell(): List<BuySell>? {
    val buySell: MutableList<BuySell> = ArrayList<BuySell>()
    try {
      val result = stat.executeQuery("SELECT * FROM buySellData")
      while(result.next()){
        val name = result.getString("stockName")
        val buy = result.getDouble("buy")
        val sell = result.getDouble("sell")
        buySell.add(BuySell(name, 0.002, buy, sell))
      }

    } catch (e: SQLException) {
      System.err.println("Couldn't select data")
      e.printStackTrace()
      return null
    }
    return buySell
  }

  fun dropAllData(){
    val deleteData = "DELETE FROM buySellData"
    try {
      stat.execute(deleteData)
    } catch (e: SQLException) {
      System.err.println("Couldn't delete data")
      e.printStackTrace()
    }
  }

}
