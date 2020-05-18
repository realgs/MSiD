import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import com.msid.stockapp.BuySell
import com.msid.stockapp.Globals
import java.util.*


class DBHelper(context: Context) : SQLiteOpenHelper(context, "stockAppDatabase", null, 1) {

  object buySellTable {
    const val name = "buySellData"
    const val stockName = "stockName"
    const val fee = "fee"
    const val buy = "buy"
    const val sell = "sell"
    const val buyCur = "buyCur"
    const val curBuyFor = "curBuyFor"
  }

  object walletTable {
    const val name = "wallets"
    const val walletName = "walletName"
    const val stockName = "stockName"
  }

  object moneyTable {
    const val name = "money"
    const val walletName = "walletName"
    const val currency = "currency"
    const val amount = "amount"
  }

  object logs {
    const val name = "transactionLogs"
    const val walletName = "walletName"
    const val time = "time"
    const val exchanged = "exchanged"
    const val bought = "bought"
    const val howMuchExchanged = "howMuchExchanged"
    const val howMuchBought = "howMuchBought"
    const val atWhatRate = "atWhatRate"
  }

  override fun onCreate(db: SQLiteDatabase?) {
    db?.execSQL("CREATE TABLE IF NOT EXISTS ${buySellTable.name} (${buySellTable.stockName} text, ${buySellTable.fee} double, " +
      "${buySellTable.buy} double, ${buySellTable.sell} double, ${buySellTable.buyCur} text, ${buySellTable.curBuyFor} text)")
    db?.execSQL("CREATE TABLE IF NOT EXISTS ${walletTable.name} " +
      "(${walletTable.walletName} text PRIMARY KEY NOT NULL, ${walletTable.stockName} text);")
    db?.execSQL("CREATE TABLE IF NOT EXISTS ${moneyTable.name} (${moneyTable.walletName} text, ${moneyTable.currency} text, ${moneyTable.amount} double," +
      "FOREIGN KEY(${walletTable.walletName}) REFERENCES ${walletTable.name})")
    db?.execSQL("CREATE TABLE IF NOT EXISTS ${logs.name} (${logs.walletName} text, ${logs.time} timestamp, ${logs.exchanged} text, ${logs.bought} text, ${logs.howMuchExchanged} double, ${logs.howMuchBought} double, ${logs.atWhatRate} double," +
      "FOREIGN KEY(${walletTable.walletName}) REFERENCES ${walletTable.name})")
  }

  override fun onUpgrade(db: SQLiteDatabase?, p1: Int, p2: Int) {}

  fun insertDataIntoBuySell(buySell: BuySell) {

    val db = this.writableDatabase

    val values = ContentValues()
    values.put(buySellTable.stockName, buySell.stockName)
    values.put(buySellTable.fee, buySell.fee)
    values.put(buySellTable.buy, buySell.buy)
    values.put(buySellTable.sell, buySell.sell)
    values.put(buySellTable.buyCur, buySell.buyCur)
    values.put(buySell.curBuyFor, buySell.curBuyFor)

    db.insert(buySellTable.name, null, values)

  }

  fun insertDataIntoWallets(walletName : String, stockName: String) {

    val db = this.writableDatabase

    val values = ContentValues()
    values.put(walletTable.walletName, walletName)
    values.put(walletTable.stockName, stockName)

    db.insert(walletTable.name, null, values)

    closeDB()

    Globals.possibleCurrencies.forEach {
      insertDataIntoMoney(walletName, it, 0.0)
    }

  }

  fun insertDataIntoMoney(walletName : String, currency:String, amount:Double) {

    val db = this.writableDatabase

    val values = ContentValues()
    values.put(moneyTable.walletName, walletName)
    values.put(moneyTable.currency, currency)
    values.put(moneyTable.amount, amount)

    db.insert(moneyTable.name, null, values)

    closeDB()

  }

  fun updateMoneyInWallet(walletName : String, currency:String, amount:Double){

    val db = this.writableDatabase

    val values = ContentValues()
    values.put(moneyTable.amount, amount)

    db.update(moneyTable.name, values, "${moneyTable.walletName}='$walletName' AND ${moneyTable.currency}='$currency'", null)
  }

  fun insertDataIntoLogs(walletName : String, exchanged: String, bought: String, howMuchExchanged: Double, howMuchBought: Double, atWhatRate: Double) {

    val db = this.writableDatabase

    val values = ContentValues()
    values.put(logs.walletName, walletName)
    values.put(logs.exchanged, exchanged)
    values.put(logs.bought, bought)
    values.put(logs.howMuchExchanged, howMuchExchanged)
    values.put(logs.howMuchBought, howMuchBought)
    values.put(logs.atWhatRate, atWhatRate)

    db.insert(logs.name, null, values)

    closeDB()

  }

  fun selectBuySell(): List<BuySell>? {
    val db = this.readableDatabase
    val buySell: MutableList<BuySell> = ArrayList<BuySell>()
    val query = "SELECT * FROM ${buySellTable.name}"

    val c = db.rawQuery(query, null)

      if(c.moveToFirst()) {
        do {
          val name = c.getString(c.getColumnIndex(buySellTable.stockName))
          val fee = c.getDouble(c.getColumnIndex(buySellTable.fee))
          val buy = c.getDouble(c.getColumnIndex(buySellTable.buy))
          val sell = c.getDouble(c.getColumnIndex(buySellTable.sell))
          val curBuy = c.getString(c.getColumnIndex(buySellTable.buyCur))
          val buyCurFor = c.getString(c.getColumnIndex(buySellTable.curBuyFor))
          buySell.add(BuySell(name, fee, buy, sell, curBuy, buyCurFor))
        } while (c.moveToNext())
      }

    closeDB()

    return buySell
  }

  fun selectWallets(): MutableList<Wallet>? {

    val db = this.readableDatabase
    val wallets: MutableList<Wallet> = mutableListOf<Wallet>()
    val query = "SELECT * FROM ${walletTable.name}"
    val c = db.rawQuery(query, null)

    //c?.moveToFirst()

    if(c.moveToFirst()) {
      do {
        val walletName = c.getString(c.getColumnIndex(walletTable.walletName))
        val stockName = c.getString(c.getColumnIndex(walletTable.stockName))
        wallets.add(Wallet(walletName, stockName, Globals.mapOfWalletStockFuns[stockName]))
      } while (c.moveToNext())
    }

    c.close()
    closeDB()

    return wallets
  }

  fun selectMoney(wallet : Wallet){
    val db = this.readableDatabase
    val query = "SELECT * FROM ${moneyTable.name} WHERE ${moneyTable.walletName} = '${wallet.name}'"
    val c = db.rawQuery(query, null)

    if(c.moveToFirst()) {
      do {
        val currency = c.getString(c.getColumnIndex(moneyTable.currency))
        val amount = c.getDouble(c.getColumnIndex(moneyTable.amount))
        wallet.currencies[currency] = amount
      } while (c.moveToNext())
    }
    c.close()
    closeDB()

  }

  fun deleteLogsData(){
    val db = this.writableDatabase
    db.delete(logs.name, null, null)
    closeDB()
  }

  fun deleteWalletData(){
    val db = this.writableDatabase
    db.delete(walletTable.name, null, null)
    db.delete(moneyTable.name, null, null)
    closeDB()
  }

  fun deleteMoneyData(){
    val db = this.writableDatabase
    db.delete(moneyTable.name, null, null)
    closeDB()
  }

  fun deleteBuySellData(){
    val db = this.writableDatabase
    db.delete(buySellTable.name, null, null)
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
