package com.example.stockapp

import BitStampTickerEntity
import BitbayTickerEntity
import BittrexTickerEntity
import CexTickerEntity
import FetchApi
import Wallet
import java.util.*

data class Response(val statusCode: Int, val body: String)
data class BuySell(
  val stockName: String,
  val fee: Double,
  val buy: Double = 0.0,
  val sell: Double = 0.0,
  val buyCur: String,
  val curBuyFor: String
)

data class Logs(
  val walletName: String,
  val time: Calendar,
  val exchanged: String,
  val bought: String,
  val howMuchExchanged: Double,
  val howMuchBought: Double,
  val atWhatRate: Double
)

object Globals {

  val bittrexStocks: List<() -> BuySell?> = listOf(
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bittrex",
        0,
        possiblePairs[0].first,
        possiblePairs[0].second,
        ::BittrexTickerEntity
      )
    },
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bittrex",
        1,
        possiblePairs[1].first,
        possiblePairs[1].second,
        ::BittrexTickerEntity
      )
    },
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bittrex",
        2,
        possiblePairs[2].first,
        possiblePairs[2].second,
        ::BittrexTickerEntity
      )
    }
  )

  val bitbayStocks: List<() -> BuySell?> = listOf(
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bitbay",
        0,
        possiblePairs[0].first,
        possiblePairs[0].second,
        ::BitbayTickerEntity
      )
    },
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bitbay",
        1,
        possiblePairs[1].first,
        possiblePairs[1].second,
        ::BitbayTickerEntity
      )
    },
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bitbay",
        2,
        possiblePairs[2].first,
        possiblePairs[2].second,
        ::BitbayTickerEntity
      )
    }
  )

  val bitstampStocks: List<() -> BuySell?> = listOf(
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bitstamp",
        0,
        possiblePairs[0].first,
        possiblePairs[0].second,
        ::BitStampTickerEntity
      )
    },
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bitstamp",
        1,
        possiblePairs[1].first,
        possiblePairs[1].second,
        ::BitStampTickerEntity
      )
    },
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "bitstamp",
        2,
        possiblePairs[2].first,
        possiblePairs[2].second,
        ::BitStampTickerEntity
      )
    }
  )

  val cexStocks: List<() -> BuySell?> = listOf(
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "cex",
        0,
        possiblePairs[0].first,
        possiblePairs[0].second,
        ::CexTickerEntity
      )
    },
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "cex",
        1,
        possiblePairs[1].first,
        possiblePairs[1].second,
        ::CexTickerEntity
      )
    },
    fun(): BuySell? {
      return FetchApi.getStockBuySell(
        "cex",
        2,
        possiblePairs[2].first,
        possiblePairs[2].second,
        ::CexTickerEntity
      )
    }
  )

  val possibleCurrencies = listOf<String>("USD", "BTC", "LTC")
  val possiblePairs = listOf<Pair<String, String>>(
    Pair(possibleCurrencies[2], possibleCurrencies[1]),
    Pair(possibleCurrencies[1], possibleCurrencies[0]),
    Pair(possibleCurrencies[2], possibleCurrencies[0])
  )

  val wallets = mutableMapOf<String, Wallet>()

  var currentWallet = Wallet("", "", null)
  var spinnerIdOfCurrentWallet = 0
  var internetConnection = false

  val mapOfWalletStockFuns = mapOf<String, List<() -> BuySell?>>(
    "bittrex" to bittrexStocks,
    "bitbay" to bitbayStocks,
    "bitstamp" to bitstampStocks,
    "cex" to cexStocks
  )

}
