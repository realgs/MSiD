import org.knowm.xchart.SwingWrapper
import org.knowm.xchart.XYChart
import org.knowm.xchart.XYChartBuilder
import javax.swing.SwingUtilities

object chartCanvas{
  private val chart =
    XYChartBuilder().width(600).height(400).title("Buy and sell values in time").xAxisTitle("Time")
      .yAxisTitle("Price").build()

  private var sellData: MutableList<Double> = ArrayList()
  private var buyData: MutableList<Double> = ArrayList()
  private val sw: SwingWrapper<XYChart> = SwingWrapper<XYChart>(chart)
  private val steps = (1..100).toList()

  private var extremeSeriesExists = false


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
      chart.updateXYSeries("AverageSell", DoubleArray(sellData.size){it.toDouble()}, DoubleArray(sellData.size){ _ -> newAverageSell}, null)
      chart.updateXYSeries("AverageBuy", DoubleArray(buyData.size){it.toDouble()}, DoubleArray(buyData.size){ _ -> newAverageBuy}, null)
      chart.updateXYSeries("SellStandardDeviation", DoubleArray(sellData.size){it.toDouble()}, DoubleArray(sellData.size){ _ -> newSellDev}, null)
      chart.updateXYSeries("BuyStandardDeviation", DoubleArray(buyData.size){it.toDouble()}, DoubleArray(buyData.size){ _ -> newBuyDev}, null)
      sw.repaintChart()
    }
  }

  fun updateThreshold(newThreshold: Double, name: String){

    if(extremeSeriesExists){
      chart.updateXYSeries(name, DoubleArray(buyData.size){it.toDouble()}, DoubleArray(buyData.size){ _ -> newThreshold}, null)
    }

    else {
      chart.addSeries(
        name,
        DoubleArray(buyData.size) { it.toDouble() },
        DoubleArray(buyData.size) { _ -> newThreshold })
        extremeSeriesExists = true
    }
    sw.repaintChart()
  }

  fun deleteThreshold(name:String){
    chart.removeSeries(name)
    extremeSeriesExists = false
  }

  fun updateChart(newSellVal:Double, newBuyVal:Double){
    if(sellData.size < 100){
      sellData.add(newSellVal)
      buyData.add(newBuyVal)

      SwingUtilities.invokeLater {
        chart.updateXYSeries("Sell", (0..sellData.size-1).toList(), sellData, null)
        chart.updateXYSeries("Buy", (0..buyData.size-1).toList(), buyData, null)
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
