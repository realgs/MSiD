import jdk.jfr.Threshold
import org.knowm.xchart.SwingWrapper
import org.knowm.xchart.XYChart
import org.knowm.xchart.XYChartBuilder
import javax.swing.SwingUtilities

object chartCanvas{
  val chart =
    XYChartBuilder().width(600).height(400).title("Buy and sell values in time").xAxisTitle("Time")
      .yAxisTitle("Price").build()

  var sellData: MutableList<Double> = ArrayList<Double>()
  var buyData: MutableList<Double> = ArrayList<Double>()
  val sw: SwingWrapper<XYChart> = SwingWrapper<XYChart>(chart)
  val steps = (1..100).toList()

  var buyExtremeSeriesExists = false
  var sellExtremeSeriesExists = false

  init{
    chart.addSeries("Sell", (1..1).toList(), arrayListOf(0))
    chart.addSeries("AverageSell", (1..1).toList(), arrayListOf(0))
    chart.addSeries("SellStandardDeviation", (1..1).toList(), arrayListOf(0))
    chart.addSeries("Buy", (1..1).toList(), arrayListOf(0))
    chart.addSeries("AverageBuy", (1..1).toList(), arrayListOf(0))
    chart.addSeries("BuyStandardDeviation", (1..1).toList(), arrayListOf(0))
    sw.displayChart()
  }

  fun updateAverage(newAverageSell: Double, newAverageBuy: Double, newSellDev: Double, newBuyDev: Double){
    val newBuyDev = newAverageBuy - newBuyDev
    val newSellDev = newAverageSell + newSellDev
    SwingUtilities.invokeLater {
      chart.updateXYSeries("AverageSell", DoubleArray(sellData.size){it.toDouble()}, DoubleArray(sellData.size){ i -> newAverageSell}, null)
      chart.updateXYSeries("AverageBuy", DoubleArray(buyData.size){it.toDouble()}, DoubleArray(buyData.size){ i -> newAverageBuy}, null)
      chart.updateXYSeries("SellStandardDeviation", DoubleArray(sellData.size){it.toDouble()}, DoubleArray(sellData.size){ i -> newSellDev}, null)
      chart.updateXYSeries("BuyStandardDeviation", DoubleArray(buyData.size){it.toDouble()}, DoubleArray(buyData.size){ i -> newBuyDev}, null)
      sw.repaintChart()
    }
  }

  fun updateBuyingThreshold(newBuyThreshold: Double){

    if(buyExtremeSeriesExists){
      chart.updateXYSeries("BuyingThreshold", DoubleArray(buyData.size){it.toDouble()}, DoubleArray(buyData.size){ i -> newBuyThreshold}, null)
    }
    else {
      chart.addSeries(
        "BuyingThreshold",
        DoubleArray(buyData.size) { it.toDouble() },
        DoubleArray(buyData.size) { i -> newBuyThreshold })
        buyExtremeSeriesExists = true
    }
    sw.repaintChart()
  }

  fun updateSellingThreshold(newSellThreshold: Double){

    if(sellExtremeSeriesExists){
      chart.updateXYSeries("SellingThreshold", DoubleArray(sellData.size){it.toDouble()}, DoubleArray(sellData.size){ i -> newSellThreshold}, null)
    }
    else {
      chart.addSeries(
        "SellingThreshold",
        DoubleArray(sellData.size) { it.toDouble() },
        DoubleArray(sellData.size) { i -> newSellThreshold })
        sellExtremeSeriesExists = true
    }
    sw.repaintChart()
  }

  fun deleteBuyingThreshold(){
    chart.removeSeries("BuyingThreshold")
    buyExtremeSeriesExists = false
  }

  fun deleteSellingThreshold(){
    chart.removeSeries("SellingThreshold")
    sellExtremeSeriesExists = false
  }

  fun updateChart(newSellVal:Double, newBuyVal:Double){
    if(sellData.size < 100){
      sellData.add(newSellVal)
      buyData.add(newBuyVal)

      SwingUtilities.invokeLater {
        chart.updateXYSeries("Sell", (1..sellData.size).toList(), sellData, null)
        chart.updateXYSeries("Buy", (1..buyData.size).toList(), buyData, null)
        sw.repaintChart()
      }
    }

    else{
      sellData = sellData.subList(1, 100)
      sellData.add(newSellVal)

      buyData = buyData.subList(1, 100)
      buyData.add(newBuyVal)

      SwingUtilities.invokeLater {
        chart.updateXYSeries("Sell", steps, sellData, null)
        chart.updateXYSeries("Buy", steps, buyData, null)
        sw.repaintChart()
      }
    }

  }

}
