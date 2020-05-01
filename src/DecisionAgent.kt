import org.apache.commons.math3.stat.descriptive.DescriptiveStatistics
import java.lang.Math.abs

object DecisionAgent {
  var wantsToBuy = true
  val dsSell: DescriptiveStatistics = DescriptiveStatistics(720)
  val dsSellChangeRate: DescriptiveStatistics = DescriptiveStatistics(720)
  val dsSellExtreme: DescriptiveStatistics = DescriptiveStatistics(36)
  val dsBuy: DescriptiveStatistics = DescriptiveStatistics(720)
  val dsBuyExtreme: DescriptiveStatistics = DescriptiveStatistics(36)
  val dsBuyChangeRate: DescriptiveStatistics = DescriptiveStatistics(720)
  var lastSellPrice = Double.MAX_VALUE
  var lastBuyPrice = 0.0
  var extreme: Double? = null

  private fun isIncreasingDrastically(newVal:Double): Boolean {
    val changeThreshold = (dsBuyChangeRate.mean + dsBuyChangeRate.standardDeviation) * -3
    println("Change threshold: ${changeThreshold}")
    println("Extreme: $extreme")

    if(extreme == null){
      extreme = newVal
      return false
    }

    chartCanvas.updateBuyingThreshold(extreme!! - changeThreshold)

    if(extreme!! - newVal > 0){
      extreme = newVal
      return false
    }

    else if (extreme!! - newVal < changeThreshold && lastBuyPrice - newVal >= changeThreshold){
      extreme = null
      return true
    }

    return false

  }

  private fun isDecreasingDrastically(newVal:Double): Boolean {
    val changeThreshold = (dsSellChangeRate.mean + dsSellChangeRate.standardDeviation) * 3
    println("Change threshold: ${changeThreshold}")
    println("Extreme: $extreme")

    if(extreme == null){
      extreme = newVal
      return false
    }

    chartCanvas.updateSellingThreshold(extreme!! - changeThreshold)

    if(extreme!! - newVal < 0){
      extreme = newVal
      return false
    }

    else if (extreme!! - newVal > changeThreshold && lastSellPrice - newVal <= changeThreshold){
      extreme = null
      return true
    }

    return false

  }

  private fun collectSellExtremeStatistics(newSellVal: Double): Boolean {
    dsSellExtreme.addValue(newSellVal)
    if(dsSellExtreme.n < 10){
      return false
    }
    val threshold = dsSellExtreme.mean - dsSellExtreme.standardDeviation
    chartCanvas.updateSellingThreshold(threshold)
    if (newSellVal < threshold) return true

    return false
  }

  private fun collectBuyExtremeStatistics(newBuyVal: Double): Boolean {
    dsBuyExtreme.addValue(newBuyVal) // we collect data from only below abnormal price
    if(dsBuyExtreme.n < 10){ // don't make any decision without enough data
      return false
    }
    val threshold = dsBuyExtreme.mean + dsBuyExtreme.standardDeviation // threshold is set to a value that considered an abnormal local grow
    chartCanvas.updateBuyingThreshold(threshold)
    if (newBuyVal > threshold) return true // if that threshold was crossed, then it is time to sell

    return false
  }


  fun makeDecision(newSellVal:Double, newBuyVal:Double): Boolean? {
    dsSell.addValue(newSellVal)
    dsBuy.addValue(newBuyVal)

    println("${dsBuy.mean} : ${dsBuy.mean - dsBuy.standardDeviation}")
    println("${dsSell.mean} : ${dsSell.mean + dsSell.standardDeviation}")

    if(dsSell.n > 2){
      dsSellChangeRate.addValue(abs(lastSellPrice - newSellVal))
      dsBuyChangeRate.addValue(abs(lastBuyPrice - newBuyVal))
    }

    chartCanvas.updateAverage(dsSell.mean, dsBuy.mean, dsSell.standardDeviation, dsBuy.standardDeviation)

    if (dsSell.n < 720) {  // make decision only if you have enough data
      lastBuyPrice = newBuyVal
      lastSellPrice = newSellVal
      println(dsSell.n)
      return null // null indicates do nothing
    }

    if (wantsToBuy) {
      if ((newBuyVal < (dsBuy.mean - dsBuy.standardDeviation) || newBuyVal <= dsBuy.min)) { // if price is abnormally low or price is as low as ever
        if(collectBuyExtremeStatistics(newBuyVal)){ // although it is worth buying it already, lets wait until it starts rising again (we reached a potential minimum)
            lastSellPrice = newSellVal
            wantsToBuy = false // you wanna sell from now on
            chartCanvas.deleteBuyingThreshold()
            dsBuyExtreme.clear()
            return true // true indicates buy
          }
        lastBuyPrice = newBuyVal
        lastSellPrice = newSellVal
        return null
      }
      chartCanvas.deleteBuyingThreshold()
      dsBuyExtreme.clear()
      extreme = null
    }
    else {
      if ((newSellVal > (dsSell.mean + dsSell.standardDeviation)) || newSellVal >= dsSell.max) { // if price is abnormally high or price is as high as ever
        if(collectSellExtremeStatistics(newSellVal)) { // although it is worth selling it already, lets wait until it starts falling again (we reached a potential maximum)
          lastBuyPrice = newBuyVal
          wantsToBuy = true // you wanna buy from now on
          chartCanvas.deleteSellingThreshold()
          dsSellExtreme.clear()
          return false // false indicates sell
        }
        lastBuyPrice = newBuyVal
        lastSellPrice = newSellVal
        return null
      }
      chartCanvas.deleteSellingThreshold()
      dsSellExtreme.clear()
      extreme = null
    }
    lastBuyPrice = newBuyVal
    lastSellPrice = newSellVal
    return null
  }
}
