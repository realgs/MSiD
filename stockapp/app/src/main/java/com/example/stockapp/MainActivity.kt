package com.example.stockapp

import DBHelper
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {
  var backPressedTime: Long = 0
  override fun onBackPressed() {
    val backToast = Toast.makeText(baseContext, "Press back again to exit", Toast.LENGTH_SHORT)
    if (backPressedTime + 2000 > System.currentTimeMillis()) {
      backToast.cancel()
      super.onBackPressed()
      return
    } else {
      backToast.show()
    }
    backPressedTime = System.currentTimeMillis()
  }

  override fun onCreate(savedInstanceState: Bundle?) {

    super.onCreate(savedInstanceState)
    setContentView(R.layout.activity_main)
    setSupportActionBar(toolbar)
    val db = DBHelper(this)
    val wal = db.selectWallets()
    if (wal.isNullOrEmpty()) db.insertDataIntoWallets("MyWallet", "bittrex")
    db.selectWallets()?.forEach {
      db.selectMoney(it)
      Globals.wallets[it.name] = it
    }
    Globals.currentWallet = Globals.wallets["MyWallet"]!!
    db.closeDB()

  }

  override fun onCreateOptionsMenu(menu: Menu): Boolean {
    menuInflater.inflate(R.menu.menu_main, menu)
    return true
  }

  override fun onOptionsItemSelected(item: MenuItem): Boolean {
    return when (item.itemId) {
      R.id.action_settings -> true
      else -> super.onOptionsItemSelected(item)
    }
  }
}
