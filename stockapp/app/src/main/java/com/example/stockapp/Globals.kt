package com.example.stockapp

import BitStampTickerEntity
import BitbayTickerEntity
import BittrexTickerEntity
import CexTickerEntity
import Wallet
import java.util.*

data class Response(val statusCode: Int, val body: String)
data class BuySell(val stockName: String, val fee: Double, val buy: Double = 0.0, val sell: Double = 0.0, val buyCur: String, val curBuyFor: String)
data class Logs(val walletName: String, val time: Calendar, val exchanged: String, val bought: String, val howMuchExchanged: Double, val howMuchBought: Double, val atWhatRate: Double)

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

  val wallets = mutableListOf<Wallet>()

  var currentWallet = Wallet("", "", null)
  var currentValueToConvertTo = possibleCurrencies[0]

  val mapOfWalletStockFuns = mapOf<String, List<() -> BuySell?>>("bittrex" to bittrexStocks, "bitbay" to bitbayStocks, "bitstamp" to bitstampStocks, "cex" to cexStocks)

}
