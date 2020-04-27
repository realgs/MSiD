import java.util.*

object DecisionAgent {
  var wantsToBuy = true
  var totalChecks = 0
  val dssSell: DoubleSummaryStatistics = DoubleSummaryStatistics()
  val dssBuy: DoubleSummaryStatistics = DoubleSummaryStatistics()
  var lastSellPrice = 0.0
  var lastBuyPrice = Double.MAX_VALUE
  var soldFor = Double.MAX_VALUE
  var boughtFor = 0.0

  fun makeDecision(newSellVal:Double, newBuyVal:Double): Boolean? {
    dssSell.accept(newSellVal)
    dssBuy.accept(newBuyVal)

    if (totalChecks++ < 100) {  // make decision only if you have enough data
      return null // null indicates do nothing
    }

    if (wantsToBuy) {
      if (((newBuyVal < dssBuy.average && lastBuyPrice < newBuyVal) || newBuyVal <= dssBuy.min) && soldFor > newBuyVal) {
        // if amount you gonna buy for is lower than amount you sold currency for last time
        // and (
        // if new buy value is lower than average buy value and price is increasing
        // or
        // new buy value is as low as ever)
        // then buy
        lastSellPrice = newSellVal
        wantsToBuy = false // you wanna sell from now on
        boughtFor = newBuyVal
        return true // true indicates buy
      }
    } else {
      if (((newSellVal > dssSell.average && lastSellPrice > newSellVal) || newSellVal >= dssSell.max) && boughtFor < newSellVal) {
        // if amount you gonna sell for is higher than amount you bought currency for last time
        // and (
        // if new sell value is higher than average sell value and price is decreasing
        // or
        // new sell value is as high as ever)
        // then sell
        lastBuyPrice = newBuyVal
        wantsToBuy = true
        soldFor = newSellVal
        return false // false indicates sell
      }
    }
    lastBuyPrice = newBuyVal
    lastSellPrice = newSellVal
    return null
  }
}
