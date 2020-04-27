class Wallet(var amount: Double, val mainCurrency: String, val investmentCurrency: String, var totalProfit: Double = 0.0) {
  private var amountOfInvestmentCurrency = 0.0
  private var boughtFor = 0.0

  fun transStockTransaction(stockToBuyOn: BuySell?, stockToSellOn: BuySell?){
    if(stockToBuyOn != null && stockToSellOn != null) {
      println("Buying on ${stockToBuyOn.stockName} and selling on ${stockToSellOn.stockName}")
      buy(stockToBuyOn.buy)
      sell(stockToSellOn.sell)
    }
  }

  fun buy(buyPrice:Double){
    amountOfInvestmentCurrency = amount / buyPrice
    boughtFor = amount
    amount = 0.0

    println("\nBought $amountOfInvestmentCurrency $investmentCurrency for $boughtFor $mainCurrency")

  }

  fun sell(sellPrice:Double){
    val soldFor = sellPrice * amountOfInvestmentCurrency
    val madeOnTransaction = soldFor - boughtFor
    totalProfit += madeOnTransaction

    println("\nSold $amountOfInvestmentCurrency $investmentCurrency for $soldFor $mainCurrency making $madeOnTransaction $mainCurrency")
    println("Total profit so far: $totalProfit $mainCurrency\nAmount of money in wallet: $soldFor $mainCurrency")

    amount = soldFor

  }


}
