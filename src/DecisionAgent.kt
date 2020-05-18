import org.apache.commons.math3.stat.descriptive.DescriptiveStatistics

object DecisionAgent {
  const val dataAge = 720 // collect data from last one hour only
  const val extremeDataAge = 36 // collect extreme data from last 3 minutes only
  const val sellThresholdPlotName = "Selling threshold"
  const val buyThresholdPlotName = "Buying threshold"

  private var wantsToBuy = true
  private val dsSell: DescriptiveStatistics = DescriptiveStatistics(dataAge)
  private val dsBuy: DescriptiveStatistics = DescriptiveStatistics(dataAge)
  private val dsExtreme: DescriptiveStatistics = DescriptiveStatistics(extremeDataAge)


  private fun collectSellExtremeStatistics(newSellVal: Double): Boolean {
    dsExtreme.addValue(newSellVal) // collect data from only above abnormal price
    if(dsExtreme.n < 10){ // don't make any decision without enough data
      return false
    }
    val threshold = dsExtreme.mean - dsExtreme.standardDeviation // threshold is set to a value that is considered an abnormal local fall
    chartCanvas.updateThreshold(threshold, sellThresholdPlotName)
    if (newSellVal < threshold) return true // if that threshold was crossed, then it is time to buy

    return false
  }

  private fun collectBuyExtremeStatistics(newBuyVal: Double): Boolean {
    dsExtreme.addValue(newBuyVal) // collect data from only below abnormal price
    if(dsExtreme.n < 10){ // don't make any decision without enough data
      return false
    }
    val threshold = dsExtreme.mean + dsExtreme.standardDeviation // threshold is set to a value that is considered an abnormal local rise
    chartCanvas.updateThreshold(threshold, buyThresholdPlotName)
    if (newBuyVal > threshold) return true // if that threshold was crossed, then it is time to sell

    return false
  }


  fun makeDecision(newSellVal:Double, newBuyVal:Double): Boolean? {
    dsSell.addValue(newSellVal)
    dsBuy.addValue(newBuyVal)

    chartCanvas.updateAverage(dsSell.mean, dsBuy.mean, dsSell.standardDeviation, dsBuy.standardDeviation)

    if (dsSell.n < dataAge) {  // make decision only if you have enough data
      return null // null indicates do nothing
    }

    if (wantsToBuy) {
      if ((newBuyVal < (dsBuy.mean - dsBuy.standardDeviation) || newBuyVal <= dsBuy.min)) { // if price is abnormally low or price is as low as ever
        if(collectBuyExtremeStatistics(newBuyVal)){ // although it is worth buying it already, lets wait until it starts rising again (we reached a potential minimum)
            wantsToBuy = false // you wanna sell from now on
            chartCanvas.deleteThreshold(buyThresholdPlotName)
            dsExtreme.clear()
            return true // true indicates buy
          }
        return null
      }
      chartCanvas.deleteThreshold(buyThresholdPlotName)
      dsExtreme.clear()
    }
    else {
      if ((newSellVal > (dsSell.mean + dsSell.standardDeviation)) || newSellVal >= dsSell.max) { // if price is abnormally high or price is as high as ever
        if(collectSellExtremeStatistics(newSellVal)) { // although it is worth selling it already, lets wait until it starts falling again (we reached a potential maximum)
          wantsToBuy = true // you wanna buy from now on
          chartCanvas.deleteThreshold(sellThresholdPlotName)
          dsExtreme.clear()
          return false // false indicates sell
        }
        return null
      }
      chartCanvas.deleteThreshold(sellThresholdPlotName)
      dsExtreme.clear()
    }
    return null
  }
}
