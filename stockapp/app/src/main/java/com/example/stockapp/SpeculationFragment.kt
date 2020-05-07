package com.example.stockapp

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.Spinner
import android.widget.Toast
import androidx.navigation.fragment.findNavController

class SpeculationFragment : Fragment() {


  override fun onCreateView(
    inflater: LayoutInflater, container: ViewGroup?,
    savedInstanceState: Bundle?
  ): View? {
    // Inflate the layout for this fragment
    return inflater.inflate(R.layout.fragment_speculation, container, false)
  }

  override fun onViewCreated(view: View, savedInstanceState: Bundle?) {

    view.findViewById<Button>(R.id.wallet_button_spec).setOnClickListener {
      findNavController().navigate(R.id.action_speculationFragment_to_WalletFragment)
    }

    val spinner: Spinner = view.findViewById(R.id.spinnerCurrencies)
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

    view.findViewById<Button>(R.id.start_button).setOnClickListener {
      val text = spinner.selectedItem.toString()
      Toast.makeText(context, text, Toast.LENGTH_SHORT).show()
    }

  }

}
