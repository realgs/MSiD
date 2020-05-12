package com.example.stockapp

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

    val job = GlobalScope.launch(Dispatchers.Main) {
      updateWorthLabel(view)
    }

//    view.findViewById<Button>(R.id.speculation_button).setOnClickListener {
//      val showCountTextView = view.findViewById<TextView>(R.id.textview_first)
//      val currentCount = showCountTextView.text.toString().toInt()
//      val action = WalletFragmentDirections.actionWalletFragmentToCurrenciesFragment(currentCount)
//      findNavController().navigate(action)
//    }

    view.findViewById<Button>(R.id.speculation_button).setOnClickListener {
      job.cancel()
      findNavController().navigate(R.id.action_WalletFragment_to_speculationFragment)
    }

    view.findViewById<Button>(R.id.currencies_button).setOnClickListener {
      job.cancel()
      findNavController().navigate(R.id.action_WalletFragment_to_CurrenciesFragment)
    }

  }

  private fun setWorthSpinner(view: View){
    val spinnerWorth: Spinner = view.findViewById(R.id.spinnerWorth)
    ArrayAdapter.createFromResource(
      view.context,
      R.array.currencies,
      android.R.layout.simple_spinner_item
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
        view.findViewById<TextView>(R.id.walletWorth).text = "Wait for it"
      }

      override fun onNothingSelected(parentView: AdapterView<*>?) {}
    }

  }

  private fun setWalletSpinner(view: View){
    val spinnerWallet: Spinner = view.findViewById(R.id.spinnerWallet)

    val adapter = ArrayAdapter<String>(view.context, android.R.layout.simple_spinner_item,
      Globals.wallets.map{ it -> it.name})
    adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)

    spinnerWallet.adapter = adapter

  }

  private suspend fun updateWorthLabel(view: View) {
      while (true) {
        val currentValue = view.findViewById<Spinner>(R.id.spinnerWorth).selectedItem.toString()
        val newVal = Globals.currentWallet.walletWorth(currentValue)
        view.findViewById<TextView>(R.id.walletWorth).text = String.format("%.2f", newVal)
        delay(5000)
    }
  }
}
