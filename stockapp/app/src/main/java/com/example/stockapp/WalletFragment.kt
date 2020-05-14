package com.example.stockapp

import DBHelper
import Wallet
import android.app.AlertDialog
import android.content.DialogInterface
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import android.widget.AdapterView.OnItemSelectedListener
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch


/**
 * A simple [Fragment] subclass as the default destination in the navigation.
 */
class WalletFragment : Fragment() {
  override fun onCreateView(
    inflater: LayoutInflater, container: ViewGroup?,
    savedInstanceState: Bundle?
  ): View? {
    // Inflate the layout for this fragment
    return inflater.inflate(R.layout.fragment_wallet, container, false)
  }

  override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    super.onViewCreated(view, savedInstanceState)

    setWorthSpinner(view)
    setWalletSpinner(view)
    setAddWalletButton(view)

    setCurrentStockLabel(view)

    val job = GlobalScope.launch(Dispatchers.Main) {
      updateWorthLabel(view)
    }

    view.findViewById<Button>(R.id.exchange_button).setOnClickListener {
      job.cancel()
      findNavController().navigate(R.id.action_WalletFragment_to_exchangeFragment)
    }

    view.findViewById<Button>(R.id.currencies_button).setOnClickListener {
      job.cancel()
      findNavController().navigate(R.id.action_WalletFragment_to_CurrenciesFragment)
    }

  }

  private fun setCurrentStockLabel(view: View){
    view.findViewById<TextView>(R.id.currenct_stock_text).text = Globals.currentWallet.stockName
  }

  private fun setWorthSpinner(view: View){
    val spinnerWorth: Spinner = view.findViewById(R.id.spinnerWorth)
    ArrayAdapter.createFromResource(
      view.context,
      R.array.currencies,
      R.layout.item_spinner
    ).also { adapter ->
      adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
      spinnerWorth.adapter = adapter
    }

    spinnerWorth.onItemSelectedListener = object : OnItemSelectedListener {
      override fun onItemSelected(
        parentView: AdapterView<*>?,
        selectedItemView: View,
        position: Int,
        id: Long
      ) {
        view.findViewById<TextView>(R.id.walletWorth).text = getString(R.string.AwaitingText)
      }

      override fun onNothingSelected(parentView: AdapterView<*>?) {}
    }

  }

  private fun setWalletSpinner(view: View){
    val spinnerWallet: Spinner = view.findViewById(R.id.spinnerWallet)
    updateWalletSpinnerContents(view)
    spinnerWallet.setSelection(Globals.spinnerIdOfCurrentWallet)

    spinnerWallet.onItemSelectedListener = object : OnItemSelectedListener {
      override fun onItemSelected(
        parentView: AdapterView<*>?,
        selectedItemView: View,
        position: Int,
        id: Long
      ) {
        Globals.currentWallet = Globals.wallets[spinnerWallet.selectedItem.toString()]!!
        view.findViewById<TextView>(R.id.walletWorth).text = getString(R.string.AwaitingText)
        setCurrentStockLabel(view)
        Globals.spinnerIdOfCurrentWallet = spinnerWallet.selectedItemPosition
      }

      override fun onNothingSelected(parentView: AdapterView<*>?) {}
    }
  }

  private fun updateWalletSpinnerContents(view: View){
    val spinner = view.findViewById<Spinner>(R.id.spinnerWallet)
    val adapter = ArrayAdapter<String>(view.context, R.layout.item_spinner,
      Globals.wallets.map{ it -> it.value.name})
    adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)

    spinner.adapter = adapter
  }


  private fun setAddWalletButton(view: View){
    val button = view.findViewById<com.google.android.material.floatingactionbutton.FloatingActionButton>(R.id.addWallet)

    button.setOnClickListener{
      val builder: AlertDialog.Builder = AlertDialog.Builder(view.context)
      builder.setTitle("Create new wallet")
      val mView: View = layoutInflater.inflate(R.layout.wallet_dialog, null)
      val mSpinner: Spinner = mView.findViewById(R.id.wallet_dialog_spinner)
      val adapter: ArrayAdapter<String> = ArrayAdapter<String>(view.context,
        android.R.layout.simple_spinner_dropdown_item,
        resources.getStringArray(R.array.stocks))
      adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
      mSpinner.adapter = adapter
      builder.setPositiveButton("Create"
      ) { _, _ -> run {
        val walletName = mView.findViewById<EditText>(R.id.wallet_dialog_edittext).text
        val stockName = mView.findViewById<Spinner>(R.id.wallet_dialog_spinner).selectedItem.toString()
        if(walletName.isNotEmpty() && !Globals.wallets.map{ it.value.name }.contains(walletName.toString())) {
              addWallet(view, walletName.toString(), stockName)
        }else{
              Toast.makeText(context, "No name provided or id name not unique", Toast.LENGTH_SHORT)
                .show()
        }
      }
      }
      builder.setNegativeButton("Cancel"
      ) { dialog, _ -> dialog.cancel() }

      builder.setView(mView)
      builder.create().show()

    }

  }

  private fun addWallet(view: View, name: String, stock: String){
    val db = DBHelper(view.context)
    db.insertDataIntoWallets(name, stock)
    val wallet = Wallet(name, stock, Globals.mapOfWalletStockFuns[stock])
    Globals.wallets.put(name, wallet)
    Globals.currentWallet = wallet
    view.findViewById<TextView>(R.id.walletWorth).text = 0.0.toString()
    updateWalletSpinnerContents(view)
    view.findViewById<Spinner>(R.id.spinnerWallet).setSelection(Globals.wallets.size-1)
    Globals.spinnerIdOfCurrentWallet = Globals.wallets.size - 1
  }

  private suspend fun updateWorthLabel(view: View) {
      while (true) {
        delay(5000)
        val currentValue = view.findViewById<Spinner>(R.id.spinnerWorth).selectedItem.toString()
        val newVal = Globals.currentWallet.walletWorth(currentValue)
        view.findViewById<TextView>(R.id.walletWorth).text = String.format("%.2f", newVal)
    }
  }
}
