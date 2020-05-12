import com.example.stockapp.BuySell
import com.example.stockapp.Globals

class Wallet(val name: String, val stockName: String,
             val stockUpdateSource: List<() -> BuySell?>?
) {

  val currencies = mutableMapOf<String, Double>(Globals.possibleCurrencies[0] to 0.0, Globals.possibleCurrencies[1] to 0.0, Globals.possibleCurrencies[2] to 0.0)

  fun transStockTransaction(sellingCur: String, buyingCur: String, stockToBuyOn: BuySell?, stockToSellOn: BuySell?){
    if(stockToBuyOn != null && stockToSellOn != null) {
      println("Buying on ${stockToBuyOn.stockName} and selling on ${stockToSellOn.stockName}")
      buy(currencies[sellingCur]!!, sellingCur, buyingCur, stockToBuyOn.buy, stockToBuyOn.fee)
      sell(currencies[buyingCur]!!, sellingCur, buyingCur, stockToSellOn.sell, stockToSellOn.fee)
    }
  }

  fun buy(amount: Double, toExchange: String, boughtCur: String, buyPrice:Double, fee:Double): String {

    if(currencies[toExchange] != null && currencies[toExchange]!! >= amount) {
      val amountBought = StockOperations.calculatePotentialBuyVal(amount, buyPrice, fee)
      currencies[boughtCur] = currencies[boughtCur]!! + amountBought
      val retVal = "\nBought $amountBought $boughtCur for ${currencies[toExchange]} $toExchange with price ${buyPrice + buyPrice * fee} $toExchange/$boughtCur"
      currencies[toExchange] = currencies[toExchange]!! - amount
      // save log to database
      // modify wallet in database
      return retVal
    }
    else{
      return "Not enough $toExchange to exchange"
    }
  }

  fun sell(amount: Double, sellingCur: String, exchangedCur: String, sellPrice:Double, fee:Double): String {
    val soldFor = StockOperations.calculatePotentialSellVal(amount, sellPrice, fee)
    if(currencies[sellingCur] != null && currencies[sellingCur]!! >= amount) {
     currencies[exchangedCur] = currencies[exchangedCur]!! + soldFor

      val retVal = "\nSold ${currencies[sellingCur]} $sellingCur for $soldFor $exchangedCur with price ${sellPrice - sellPrice * fee} $exchangedCur/$sellingCur"

      currencies[sellingCur] = currencies[sellingCur]!! - amount

      return retVal
    }
    else{
      return "Not enough $sellingCur to sell"
    }
  }

  suspend fun walletWorth(currencyToDisplay: String): Double {
    var totalWorth = currencies[currencyToDisplay]!!
    if(stockUpdateSource != null) {
      val stockResults = StockOperations.watchAllStocks(stockUpdateSource)
      stockResults.forEach {
        if (it != null) {
          if (it.buyCur == currencyToDisplay) {
            totalWorth += StockOperations.calculatePotentialBuyVal(currencies[it.curBuyFor]!!, it.buy, it.fee)
          } else if (it.curBuyFor == currencyToDisplay) {
            totalWorth += StockOperations.calculatePotentialSellVal(currencies[it.buyCur]!!, it.sell, it.fee)
          }
        }
      }
    }
  return totalWorth
  }


}
