package com.example.stockapp

import DBHelper
import android.app.AlertDialog
import android.os.Bundle
import android.text.InputType
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController


class CurrenciesFragment : Fragment() {
  private val decimalPlaces = 4

  override fun onCreateView(
    inflater: LayoutInflater, container: ViewGroup?,
    savedInstanceState: Bundle?
  ): View? {
    return inflater.inflate(R.layout.fragment_currencies, container, false)
  }

  override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    super.onViewCreated(view, savedInstanceState)

    view.findViewById<Button>(R.id.wallet_button_cur).setOnClickListener {
      findNavController().navigate(R.id.action_CurrenciesFragment_to_WalletFragment)
    }

    setCurrenciesSpinner(view)

    setCurrencyAmountLabel(view, view.findViewById<Spinner>(R.id.spinnerCurrenciesToExchange))

    view.findViewById<com.google.android.material.floatingactionbutton.FloatingActionButton>(R.id.addCurrency)
      .setOnClickListener {
        addAmountOfCurrency(view)
      }
  }

  private fun setCurrencyAmountLabel(view: View, spinner: Spinner) {
    val currentCurrency = spinner.selectedItem.toString()
    val amount = Globals.currentWallet.currencies[currentCurrency]
    view.findViewById<TextView>(R.id.currency_amount).text =
      String.format("%.${decimalPlaces}f", amount)
  }

  private fun setCurrenciesSpinner(view: View) {
    val spinnerCurrencies: Spinner = view.findViewById(R.id.spinnerCurrenciesToExchange)
    ArrayAdapter.createFromResource(
      view.context,
      R.array.currencies,
      R.layout.item_spinner
    ).also { adapter ->
      adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
      spinnerCurrencies.adapter = adapter
    }

    spinnerCurrencies.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
      override fun onItemSelected(
        parentView: AdapterView<*>?,
        selectedItemView: View,
        position: Int,
        id: Long
      ) {
        setCurrencyAmountLabel(view, spinnerCurrencies)
      }

      override fun onNothingSelected(parentView: AdapterView<*>?) {}
    }
  }

  private fun addAmountOfCurrency(view: View) {
    var amount: Double
    val currency =
      view.findViewById<Spinner>(R.id.spinnerCurrenciesToExchange).selectedItem.toString()

    val builder: AlertDialog.Builder = AlertDialog.Builder(view.context)
    builder.setTitle("Add amount of $currency to ${Globals.currentWallet.name}")

    val input = EditText(context)
    input.inputType = InputType.TYPE_CLASS_NUMBER or InputType.TYPE_NUMBER_FLAG_DECIMAL
    builder.setView(input)

    builder.setPositiveButton(
      "OK"
    ) { _, _ ->
      run {
        val typed = input.text.toString()
        if (typed != "." && typed.isNotEmpty()) {
          amount = typed.toDouble()
          addAmountAfterConfirm(view, amount, currency)
          view.findViewById<TextView>(R.id.currency_amount).text =
            String.format("%.${decimalPlaces}f", Globals.currentWallet.currencies[currency])
        }
      }
    }
    builder.setNegativeButton(
      "Cancel"
    ) { dialog, _ -> dialog.cancel() }

    builder.show()
  }

  private fun addAmountAfterConfirm(view: View, amount: Double, currency: String) {
    val newValue = Globals.currentWallet.currencies[currency]!! + amount
    Globals.currentWallet.currencies[currency] = newValue
    val db = DBHelper(view.context)
    db.insertDataIntoMoney(Globals.currentWallet.name, currency, newValue)
    db.closeDB()
  }

}
