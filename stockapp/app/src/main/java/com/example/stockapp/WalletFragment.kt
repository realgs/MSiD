package com.example.stockapp

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.navigation.fragment.findNavController

/**
 * A simple [Fragment] subclass as the default destination in the navigation.
 */
class WalletFragment : Fragment() {

  private fun countMe(view: View) {
    val showCountTextView = view.findViewById<TextView>(R.id.textview_first)
    val countString = showCountTextView.text.toString()
    var count = countString.toInt()
    count++
    showCountTextView.text = count.toString()
  }

  override fun onCreateView(
    inflater: LayoutInflater, container: ViewGroup?,
    savedInstanceState: Bundle?
  ): View? {
    // Inflate the layout for this fragment
    return inflater.inflate(R.layout.fragment_wallet, container, false)
  }

  override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    super.onViewCreated(view, savedInstanceState)

//    view.findViewById<Button>(R.id.speculation_button).setOnClickListener {
//      val showCountTextView = view.findViewById<TextView>(R.id.textview_first)
//      val currentCount = showCountTextView.text.toString().toInt()
//      val action = WalletFragmentDirections.actionWalletFragmentToCurrenciesFragment(currentCount)
//      findNavController().navigate(action)
//    }

    view.findViewById<Button>(R.id.speculation_button).setOnClickListener {
      findNavController().navigate(R.id.action_WalletFragment_to_speculationFragment)
    }

    view.findViewById<Button>(R.id.currencies_button).setOnClickListener {
      findNavController().navigate(R.id.action_WalletFragment_to_CurrenciesFragment)
    }

    val spinner: Spinner = view.findViewById(R.id.spinner)
// Create an ArrayAdapter using the string array and a default spinner layout
    ArrayAdapter.createFromResource(
      view.context,
      R.array.currencies,
      android.R.layout.simple_spinner_item
    ).also { adapter ->
      // Specify the layout to use when the list of choices appears
      adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
      // Apply the adapter to the spinner
      spinner.adapter = adapter
    }

  }
}
