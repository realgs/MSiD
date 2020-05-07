package com.example.stockapp

import android.app.AlertDialog
import android.content.DialogInterface
import android.os.Bundle
import android.text.InputType
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.navigation.fragment.navArgs


/**
 * A simple [Fragment] subclass as the second destination in the navigation.
 */
class CurrenciesFragment : Fragment() {

  override fun onCreateView(
    inflater: LayoutInflater, container: ViewGroup?,
    savedInstanceState: Bundle?
  ): View? {
    // Inflate the layout for this fragment
    return inflater.inflate(R.layout.fragment_currencies, container, false)
  }

  //val args: CurrenciesFragmentArgs by navArgs()

  fun addAmountOfCurrency(view: View){
    var amount = 0

    Toast.makeText(context, "Adding currency", Toast.LENGTH_SHORT).show()
    val builder: AlertDialog.Builder = AlertDialog.Builder(view.context)
    builder.setTitle("Title")


    val input = EditText(context)
    input.inputType = InputType.TYPE_NUMBER_FLAG_DECIMAL
    builder.setView(input)

    builder.setPositiveButton("OK",
      DialogInterface.OnClickListener { dialog, which -> amount = input.text.toString().toInt() })
    builder.setNegativeButton("Cancel",
      DialogInterface.OnClickListener { dialog, which -> dialog.cancel() })

    builder.show()
  }

  override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    super.onViewCreated(view, savedInstanceState)

    view.findViewById<Button>(R.id.wallet_button_cur).setOnClickListener {
      findNavController().navigate(R.id.action_CurrenciesFragment_to_WalletFragment)
    }

    view.findViewById<com.google.android.material.floatingactionbutton.FloatingActionButton>(R.id.addCurrency).setOnClickListener {

    }

//    val count = args.myArg
//    val countText = getString(R.string.currencies_header, count)
//    view.findViewById<TextView>(R.id.currencies_header).text = countText


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

  }
}
