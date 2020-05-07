package com.example.stockapp

import BitStampTickerEntity
import BitbayTickerEntity
import BittrexTickerEntity
import BuySell
import CexTickerEntity
import Wallet

object Globals {

  val bittrexStocks: List<() -> BuySell?> = listOf(
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bittrex",
        0,
        "BTC",
        "LTC",
        ::BittrexTickerEntity
      )
    },
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bittrex",
        1,
        "BTC",
        "USD",
        ::BittrexTickerEntity
      )
    },
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bittrex",
        2,
        "LTC",
        "USD",
        ::BittrexTickerEntity
      )
    }
  )

  val bitbayStocks: List<() -> BuySell?> = listOf(
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bitbay",
        0,
        "BTC",
        "LTC",
        ::BitbayTickerEntity
      )
    },
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bitbay",
        1,
        "BTC",
        "USD",
        ::BitbayTickerEntity
      )
    },
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bitbay",
        2,
        "LTC",
        "USD",
        ::BitbayTickerEntity
      )
    }
  )

  val bitstampStocks: List<() -> BuySell?> = listOf(
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bitstamp",
        0,
        "BTC",
        "LTC",
        ::BitStampTickerEntity
      )
    },
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bitstamp",
        1,
        "BTC",
        "USD",
        ::BitStampTickerEntity
      )
    },
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bitstamp",
        2,
        "LTC",
        "USD",
        ::BitStampTickerEntity
      )
    }
  )

  val cexStocks: List<() -> BuySell?> = listOf(
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "cex",
        0,
        "BTC",
        "LTC",
        ::CexTickerEntity) },
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "cex",
        1,
        "BTC",
        "USD",
        ::CexTickerEntity) },
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "cex",
        2,
        "LTC",
        "USD",
        ::CexTickerEntity) }
  )

  val possibleCurrencies = listOf<String>("USD", "BTC", "LTC")
  val possiblePairs = listOf<Pair<String, String>>(Pair(possibleCurrencies[2], possibleCurrencies[1]), Pair(possibleCurrencies[1], possibleCurrencies[0]), Pair(possibleCurrencies[2], possibleCurrencies[0]))

  val bittrexWallet = Wallet()
  val bitbayWallet = Wallet()
  val bitstampWallet = Wallet()
  val cexWallet = Wallet()


  var currentWallet = bittrexWallet
  var currentValueToConvertTo = possibleCurrencies[0]

  val stockWalletMap = mapOf<Wallet, List<() -> BuySell?>>(bittrexWallet to bittrexStocks, bitbayWallet to bitbayStocks, bitstampWallet to bitstampStocks, cexWallet to cexStocks)

}
