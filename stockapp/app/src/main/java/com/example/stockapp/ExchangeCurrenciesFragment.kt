package com.example.stockapp

import DBHelper
import StockOperations
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class ExchangeCurrenciesFragment : Fragment() {
  var lastStockResults: List<BuySell?>? = null

  override fun onCreateView(
    inflater: LayoutInflater, container: ViewGroup?,
    savedInstanceState: Bundle?
  ): View? {
    // Inflate the layout for this fragment
    return inflater.inflate(R.layout.fragment_exchange, container, false)
  }

  override fun onViewCreated(view: View, savedInstanceState: Bundle?) {

    addCurrenciesToExchangeSpinner(view)
    addCurrenciesToReceiveSpinner(view)
    addExchangeButton(view)

    updateExchangeText(view)
    updateReceiveText(view, null)

    configureExchangeText(view)


    val job = GlobalScope.launch(Dispatchers.Main) {
      checkValue(view)
    }

    view.findViewById<Button>(R.id.wallet_button_spec).setOnClickListener {
      job.cancel()
      findNavController().navigate(R.id.action_speculationFragment_to_WalletFragment)
    }

  }

  suspend fun checkValue(view: View): Double {
    var amountToReceive: Double?
    while (true) {
      delay(5000)
      val currencyToExchange =
        view.findViewById<Spinner>(R.id.spinnerCurrenciesToExchange).selectedItem.toString()
      val currencyToReceive =
        view.findViewById<Spinner>(R.id.spinnerCurrenciesToReceive).selectedItem.toString()
      val amount = view.findViewById<EditText>(R.id.amountToExchange).text
      if (amount.isNotEmpty()) {
        lastStockResults = StockOperations.watchAllStocks(Globals.currentWallet.stockUpdateSource!!)
        if (amount.toString() != ".") {
          if (currencyToExchange != currencyToReceive) {
            amountToReceive =
              getWorthiness(currencyToExchange, currencyToReceive, amount.toString().toDouble())
            if (amountToReceive != null) {
              updateReceiveText(view, amountToReceive)
            }
          } else {
            updateReceiveText(view, amount.toString().toDouble())
          }
        } else {
          updateReceiveText(view, null)
        }
      }
    }
  }

  fun getWorthiness(
    currencyToExchange: String,
    currencyToReceive: String,
    amount: Double
  ): Double? {
    lastStockResults?.forEach {
      if (it != null) {
        if (it.curBuyFor == currencyToExchange && it.buyCur == currencyToReceive) {
          return StockOperations.calculatePotentialBuyVal(amount, it.sell, it.fee)
        } else if (it.curBuyFor == currencyToReceive && it.buyCur == currencyToExchange) {
          return StockOperations.calculatePotentialSellVal(amount, it.sell, it.fee)
        }
      }
    }
    return null
  }

  fun configureExchangeText(view: View) {
    view.findViewById<EditText>(R.id.amountToExchange).addTextChangedListener(object : TextWatcher {
      override fun afterTextChanged(p0: Editable?) {}

      override fun beforeTextChanged(p0: CharSequence?, p1: Int, p2: Int, p3: Int) {}

      override fun onTextChanged(p0: CharSequence?, p1: Int, p2: Int, p3: Int) {
        val curToExchange =
          view.findViewById<Spinner>(R.id.spinnerCurrenciesToExchange).selectedItem.toString()
        val curToReceive =
          view.findViewById<Spinner>(R.id.spinnerCurrenciesToReceive).selectedItem.toString()
        val amount = view.findViewById<EditText>(R.id.amountToExchange).text
        if (amount.isNotEmpty() && amount.toString() != ".") {
          if (curToExchange == curToReceive) {
            updateReceiveText(view, amount.toString().toDouble())
          } else {
            val newReceiveAmount =
              getWorthiness(curToExchange, curToReceive, amount.toString().toDouble())
            updateReceiveText(view, newReceiveAmount)
          }
        } else {
          updateReceiveText(view, null)
        }

      }

    })
  }

  fun updateExchangeText(view: View) {
    val currency =
      view.findViewById<Spinner>(R.id.spinnerCurrenciesToExchange).selectedItem.toString()
    val field = view.findViewById<EditText>(R.id.amountToExchange)
    field.text.clear()
    field.append(Globals.currentWallet.currencies[currency].toString())
  }

  fun updateReceiveText(view: View, amount: Double?) {
    val field = view.findViewById<EditText>(R.id.amountReceived)
    field.text.clear()
    if (amount != null) {
      field.append(amount.toString())
    } else {
      field.append("Unknown")
    }

  }

  fun addExchangeButton(view: View) {
    view.findViewById<com.google.android.material.floatingactionbutton.FloatingActionButton>(R.id.exchangeButton)
      .setOnClickListener {
        val exchangeAmount = view.findViewById<EditText>(R.id.amountToExchange).text
        val currencyToExchange =
          view.findViewById<Spinner>(R.id.spinnerCurrenciesToExchange).selectedItem.toString()
        val currencyToReceive =
          view.findViewById<Spinner>(R.id.spinnerCurrenciesToReceive).selectedItem.toString()
        if (exchangeAmount.isNotEmpty()) {
          if (currencyToExchange == currencyToReceive) {
            Toast.makeText(context, "It is indeed an exquisite transaction", Toast.LENGTH_SHORT)
              .show()
          } else {
            if (exchangeAmount.toString() != "." && exchangeAmount.isNotEmpty()) {
              lastStockResults?.forEach {
                if (it != null) {
                  if (it.curBuyFor == currencyToExchange && it.buyCur == currencyToReceive) {
                    val enoughMoney = Globals.currentWallet.buy(
                      exchangeAmount.toString().toDouble(),
                      currencyToExchange,
                      currencyToReceive,
                      it.buy,
                      it.fee
                    )
                    if (enoughMoney) {
                      updateMoneyInDB(view, currencyToExchange, currencyToReceive)
                    } else {
                      Toast.makeText(context, "Insufficient funds", Toast.LENGTH_SHORT).show()
                    }

                  } else if (it.curBuyFor == currencyToReceive && it.buyCur == currencyToExchange) {
                    val enoughMoney = Globals.currentWallet.sell(
                      exchangeAmount.toString().toDouble(),
                      currencyToExchange,
                      currencyToReceive,
                      it.sell,
                      it.fee
                    )
                    if (enoughMoney) {
                      updateMoneyInDB(view, currencyToExchange, currencyToReceive)
                    } else {
                      Toast.makeText(context, "Insufficient funds", Toast.LENGTH_SHORT).show()
                    }
                  }
                } else {
                  Toast.makeText(
                    context,
                    "Stock is not available for some reason. Try again later",
                    Toast.LENGTH_SHORT
                  ).show()
                }
              }
            }
          }

        }
      }
  }

  fun updateMoneyInDB(view: View, currencyToExchange: String, currencyToReceive: String) {
    val db = DBHelper(view.context)
    Toast.makeText(context, "Exchange successful", Toast.LENGTH_SHORT).show()
    updateExchangeText(view)
    db.updateMoneyInWallet(
      Globals.currentWallet.name, currencyToReceive,
      Globals.currentWallet.currencies[currencyToReceive]!!
    )
    db.updateMoneyInWallet(
      Globals.currentWallet.name, currencyToExchange,
      Globals.currentWallet.currencies[currencyToExchange]!!
    )
  }

  fun addCurrenciesToExchangeSpinner(view: View) {
    val spinner: Spinner = view.findViewById(R.id.spinnerCurrenciesToExchange)
    ArrayAdapter.createFromResource(
      view.context,
      R.array.currencies,
      R.layout.item_spinner
    ).also { adapter ->
      adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
      spinner.adapter = adapter
    }

    spinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
      override fun onItemSelected(
        parentView: AdapterView<*>?,
        selectedItemView: View,
        position: Int,
        id: Long
      ) {
        updateExchangeText(view)
      }

      override fun onNothingSelected(parentView: AdapterView<*>?) {}
    }
  }

  fun addCurrenciesToReceiveSpinner(view: View) {
    val spinner: Spinner = view.findViewById(R.id.spinnerCurrenciesToReceive)
    ArrayAdapter.createFromResource(
      view.context,
      R.array.currencies,
      R.layout.item_spinner
    ).also { adapter ->
      adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
      spinner.adapter = adapter
    }

    spinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
      override fun onItemSelected(
        parentView: AdapterView<*>?,
        selectedItemView: View,
        position: Int,
        id: Long
      ) {
        val amount = view.findViewById<EditText>(R.id.amountToExchange).text.toString()
        if (amount != "." && amount.isNotEmpty()) {
          val currencyToExchange =
            view.findViewById<Spinner>(R.id.spinnerCurrenciesToExchange).selectedItem.toString()
          val currencyToReceive =
            view.findViewById<Spinner>(R.id.spinnerCurrenciesToReceive).selectedItem.toString()
          val field = view.findViewById<EditText>(R.id.amountReceived)
          field.text.clear()
          if (currencyToExchange == currencyToReceive) {
            field.append(amount.toString())
          } else {
            val receiveAmount =
              getWorthiness(currencyToExchange, currencyToReceive, amount.toDouble())
            updateReceiveText(view, receiveAmount)
          }
        } else updateReceiveText(view, null)
      }

      override fun onNothingSelected(parentView: AdapterView<*>?) {}
    }
  }

}
