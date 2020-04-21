class Wallet(var amount: Double, val mainCurrency: String, val investmentCurrency: String, var totalProfit: Double = 0.0) {
  fun transaction(stockToBuyOn: BuySell?, stockToSellOn: BuySell?){
    if(stockToBuyOn != null && stockToSellOn != null) {
      val amountBought = amount / stockToBuyOn.buy
      val soldFor = stockToSellOn.sell * amountBought
      val madeOnTransaction = soldFor - amount
      totalProfit += madeOnTransaction
      amount = soldFor

      println("\nBought $amountBought $investmentCurrency for $amount $mainCurrency and sold them for $soldFor $mainCurrency making $madeOnTransaction $mainCurrency")
      println("Total profit so far: $totalProfit $mainCurrency\nAmount of money in wallet: $amount $mainCurrency")
    }
  }
}
