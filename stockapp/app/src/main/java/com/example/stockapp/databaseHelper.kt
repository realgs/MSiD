import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import com.example.stockapp.BuySell
import com.example.stockapp.Globals
import java.util.*


class DBHelper(context: Context) : SQLiteOpenHelper(context, "stockAppDatabase", null, 1) {

  override fun onCreate(db: SQLiteDatabase?) {
    db?.execSQL("CREATE TABLE IF NOT EXISTS buySellData (stockName text, fee double, " +
      "buy double, sell double, buyCur text, curBuyFor text)")
    db?.execSQL("CREATE TABLE IF NOT EXISTS wallets " +
      "(walletName text PRIMARY KEY NOT NULL, stockName text);")
    db?.execSQL("CREATE TABLE IF NOT EXISTS money (walletName text, currency text, amount double," +
      "FOREIGN KEY(walletName) REFERENCES wallets)")
    db?.execSQL("CREATE TABLE IF NOT EXISTS transactionLogs (walletName text, time timestamp, exchanged text, bought text, howMuchExchanged double, howMuchBought double, atWhatRate double," +
      "FOREIGN KEY(walletName) REFERENCES wallets)")

    println("Created successfully")
  }

  override fun onUpgrade(db: SQLiteDatabase?, p1: Int, p2: Int) {}

  fun createBuySellTable(db: SQLiteDatabase?){
    val createTable ="CREATE TABLE IF NOT EXISTS buySellData (stockName text, fee double, " +
      "buy double, sell double, buyCur text, curBuyFor text)"
      db?.execSQL(createTable)
    closeDB()
  }

  fun createWalletsTable(db: SQLiteDatabase?){
    val createTable = "CREATE TABLE IF NOT EXISTS wallets " +
    "(walletName text PRIMARY KEY NOT NULL, stockName text);"
      db?.execSQL(createTable)

    closeDB()

    if(selectWallets().isNullOrEmpty()){
      insertDataIntoWallets("myWallet", "bittrex")
    }

  }

  fun createMoneyTable(db: SQLiteDatabase?){
    val createTable =
      "CREATE TABLE IF NOT EXISTS money (walletName text, currency text, amount double," +
        "FOREIGN KEY(walletName) REFERENCES wallets)"
    db?.execSQL(createTable)
    closeDB()
  }

  fun createTransactionLogs(db: SQLiteDatabase?){
    val createTable =
      "CREATE TABLE IF NOT EXISTS transactionLogs (walletName text, time timestamp, exchanged text, bought text, howMuchExchanged double, howMuchBought double, atWhatRate double," +
        "FOREIGN KEY(walletName) REFERENCES wallets)"
    db?.execSQL(createTable)
    closeDB()
  }

  fun insertDataIntoBuySell(buySell: BuySell) {

    val db = this.writableDatabase

    val values = ContentValues()
    values.put("stockName", buySell.stockName)
    values.put("fee", buySell.fee)
    values.put("buy", buySell.buy)
    values.put("sell", buySell.sell)
    values.put("buyCur", buySell.buyCur)
    values.put("curBuyFor", buySell.curBuyFor)

    db.insert("buySellData", null, values)

  }

  fun insertDataIntoWallets(walletName : String, stockName: String) {

    val db = this.writableDatabase

    val values = ContentValues()
    values.put("walletName", walletName)
    values.put("stockName", stockName)

    db.insert("wallets", null, values)

    closeDB()

    Globals.possibleCurrencies.forEach {
      insertDataIntoMoney(walletName, it, 0.0)
    }

  }

  fun insertDataIntoMoney(walletName : String, currency:String, amount:Double) {

    val db = this.writableDatabase

    val values = ContentValues()
    values.put("walletName", walletName)
    values.put("currency", currency)
    values.put("amount", amount)

    db.insert("money", null, values)

    closeDB()

  }

  fun updateMoneyInWallet(walletName : String, currency:String, amount:Double){

    val db = this.writableDatabase

    val values = ContentValues()
    values.put("walletName", walletName)
    values.put("currency", currency)
    values.put("amount", amount)

    db.update("money", values, "currency='$currency'", null)
  }

  fun insertDataIntoLogs(walletName : String, exchanged: String, bought: String, howMuchExchanged: Double, howMuchBought: Double, atWhatRate: Double) {

    val db = this.writableDatabase

    val values = ContentValues()
    values.put("walletName", walletName)
    values.put("exchanged", exchanged)
    values.put("bought", bought)
    values.put("howMuchExchanged", howMuchExchanged)
    values.put("howMuchBought", howMuchBought)
    values.put("atWhatRate", atWhatRate)

    db.insert("transactionLogs", null, values)

    closeDB()

  }

  fun selectBuySell(): List<BuySell>? {
    val db = this.readableDatabase
    val buySell: MutableList<BuySell> = ArrayList<BuySell>()
    val query = "SELECT * FROM buySellData"

    val c = db.rawQuery(query, null)

      if(c.moveToFirst()) {
        do {
          val name = c.getString(c.getColumnIndex("stockName"))
          val fee = c.getDouble(c.getColumnIndex("fee"))
          val buy = c.getDouble(c.getColumnIndex("buy"))
          val sell = c.getDouble(c.getColumnIndex("sell"))
          val curBuy = c.getString(c.getColumnIndex("curBuy"))
          val buyCurFor = c.getString(c.getColumnIndex("buyCurFor"))
          buySell.add(BuySell(name, fee, buy, sell, curBuy, buyCurFor))
        } while (c.moveToNext())
      }

    closeDB()

    return buySell
  }

  fun selectWallets(): MutableList<Wallet>? {

    val db = this.readableDatabase
    val wallets: MutableList<Wallet> = mutableListOf<Wallet>()
    val query = "SELECT * FROM wallets"
    val c = db.rawQuery(query, null)

    c?.moveToFirst()

    if(c.moveToFirst()) {
      do {
        val walletName = c.getString(c.getColumnIndex("walletName"))
        val stockName = c.getString(c.getColumnIndex("stockName"))
        wallets.add(Wallet(walletName, stockName, Globals.mapOfWalletStockFuns[stockName]))
      } while (c.moveToNext())
    }

    c.close()
    closeDB()

    return wallets
  }

  fun selectMoney(wallet : Wallet){
    val db = this.readableDatabase
    val query = "SELECT * FROM money WHERE walletName = '${wallet.name}'"
    val c = db.rawQuery(query, null)

    if(c.moveToFirst()) {
      do {
        val currency = c.getString(c.getColumnIndex("currency"))
        val amount = c.getDouble(c.getColumnIndex("amount"))
        wallet.currencies[currency] = amount
      } while (c.moveToNext())
    }
    c.close()
    closeDB()

  }

  fun deleteLogsData(){
    val db = this.writableDatabase
    db.delete("transactionLogs", null, null)
    closeDB()
  }

  fun deleteWalletData(){
    val db = this.writableDatabase
    db.delete("wallets", null, null)
    db.delete("money", null, null)
    closeDB()
  }

  fun deleteMoneyData(){
    val db = this.writableDatabase
    db.delete("money", null, null)
    closeDB()
  }

  fun deleteBuySellData(){
    val db = this.writableDatabase
    db.delete("buySellData", null, null)
    closeDB()
  }

  fun clearDB(){
    deleteWalletData()
    deleteMoneyData()
    deleteLogsData()
    deleteBuySellData()
  }

  fun closeDB() {
    val db = this.readableDatabase
    if (db != null && db.isOpen) db.close()
  }

}
