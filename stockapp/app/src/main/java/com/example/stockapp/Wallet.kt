class Wallet(var amount: Double, val mainCurrency: String, val investmentCurrency: String, var totalProfit: Double = 0.0) {
  private var amountOfInvestmentCurrency = 0.0
  private var boughtFor = 0.0

  fun transStockTransaction(stockToBuyOn: BuySell?, stockToSellOn: BuySell?){
    if(stockToBuyOn != null && stockToSellOn != null) {
      println("Buying on ${stockToBuyOn.stockName} and selling on ${stockToSellOn.stockName}")
      buy(stockToBuyOn.buy, stockToBuyOn.fee)
      sell(stockToSellOn.sell, stockToSellOn.fee)
    }
  }

  fun buy(buyPrice:Double, fee:Double){
    amountOfInvestmentCurrency = (amount / buyPrice) - ((amount / buyPrice) * fee)
    boughtFor = amount
    amount = 0.0

    println("\nBought $amountOfInvestmentCurrency $investmentCurrency for $boughtFor $mainCurrency with price ${buyPrice + buyPrice * fee} $mainCurrency/$investmentCurrency")

  }

  fun sell(sellPrice:Double, fee:Double){
    val soldFor = sellPrice * amountOfInvestmentCurrency - (sellPrice * amountOfInvestmentCurrency * fee)
    val madeOnTransaction = soldFor - boughtFor
    totalProfit += madeOnTransaction

    println("\nSold $amountOfInvestmentCurrency $investmentCurrency for $soldFor $mainCurrency with price ${sellPrice - sellPrice * fee} $mainCurrency/$investmentCurrency making $madeOnTransaction $mainCurrency")
    println("Total profit so far: $totalProfit $mainCurrency\nAmount of money in wallet: $soldFor $mainCurrency")

    amount = soldFor

  }


}
