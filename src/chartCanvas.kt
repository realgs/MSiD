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

  init{
    chart.addSeries("Sell", (1..1).toList(), arrayListOf(0))
    chart.addSeries("Buy", (1..1).toList(), arrayListOf(0))
    sw.displayChart()
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
