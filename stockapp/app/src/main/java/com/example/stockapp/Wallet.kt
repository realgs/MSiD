import com.example.stockapp.Globals

class Wallet() {

  val currencies = mutableMapOf<String, Double>(Globals.possibleCurrencies[0] to 0.0, Globals.possibleCurrencies[1] to 1.0, Globals.possibleCurrencies[2] to 0.0)

  fun transStockTransaction(sellingCur: String, buyingCur: String, stockToBuyOn: BuySell?, stockToSellOn: BuySell?){
    if(stockToBuyOn != null && stockToSellOn != null) {
      println("Buying on ${stockToBuyOn.stockName} and selling on ${stockToSellOn.stockName}")
      buy(sellingCur, buyingCur, stockToBuyOn.buy, stockToBuyOn.fee)
      sell(sellingCur, buyingCur, stockToSellOn.sell, stockToSellOn.fee)
    }
  }

  fun buy(toExchange: String, boughtCur: String, buyPrice:Double, fee:Double): String {
    if(currencies[toExchange] != null && currencies[toExchange]!! > 0) {
      val amountBought =
        (currencies[toExchange]!! / buyPrice) + ((currencies[toExchange]!! / buyPrice) * fee)
      currencies[boughtCur] = currencies[boughtCur]!! + amountBought
      val retVal = "\nBought $amountBought $boughtCur for ${currencies[toExchange]} $toExchange with price ${buyPrice + buyPrice * fee} $toExchange/$boughtCur"
      currencies[toExchange] = 0.0
      // save log to database
      return retVal
    }
    else{
      return "Not enough $toExchange to exchange"
    }
  }

  fun sell(sellingCur: String, exchangedCur: String, sellPrice:Double, fee:Double): String {
    if(currencies[sellingCur] != null && currencies[sellingCur]!! > 0) {
      val soldFor =
        sellPrice * currencies[sellingCur]!! - (sellPrice * currencies[sellingCur]!! * fee)
     currencies[exchangedCur] = currencies[exchangedCur]!! + soldFor

      val retVal = "\nSold ${currencies[sellingCur]} $sellingCur for $soldFor $exchangedCur with price ${sellPrice - sellPrice * fee} $exchangedCur/$sellingCur"

      currencies[sellingCur] = 0.0

      return retVal
    }
    else{
      return "Not enough $sellingCur to sell"
    }
  }

  fun calculatePotentialSellVal(amountToSell: Double, sellPrice:Double, fee:Double): Double {

    return sellPrice * amountToSell - (sellPrice * amountToSell * fee)
  }

  fun calculatePotentialBuyVal(amountToBuy: Double, buyPrice:Double, fee:Double): Double {
    return (amountToBuy / buyPrice) + ((amountToBuy / buyPrice) * fee)
  }

  suspend fun walletWorth(currencyToDisplay: String, currentStockUpdateSource: List<() -> BuySell?>): Double {
    var totalWorth = currencies[currencyToDisplay]!!
    val stockResults = StockOperations.watchAllStocks(currentStockUpdateSource)
    stockResults.forEach{
      if(it != null){
        if(it.buyCur == currencyToDisplay){
          println("$it selling")
          totalWorth += calculatePotentialBuyVal(currencies[it.curBuyFor]!!, it.buy, it.fee)
        }
        else if(it.curBuyFor == currencyToDisplay){
          println("$it buying")
          totalWorth += calculatePotentialSellVal(currencies[it.buyCur]!!, it.sell, it.fee)
        }
      }
    }
  return totalWorth
  }


}
