import org.knowm.xchart.SwingWrapper
import org.knowm.xchart.OHLCChart
import org.knowm.xchart.OHLCChartBuilder
import kotlin.collections.ArrayList

class ChartCanvas(val title: String, dataset: List<ChartData>){

  private val chart =
    OHLCChartBuilder().width(600).height(400).title(title)
      .xAxisTitle("Time").build()

  private var highData: MutableList<Double> = ArrayList()
  private var lowData: MutableList<Double> = ArrayList()
  private var openData: MutableList<Double> = ArrayList()
  private var closeData: MutableList<Double> = ArrayList()
  private val sw: SwingWrapper<OHLCChart> = SwingWrapper<OHLCChart>(chart)

  init{
    for (data in dataset) {
      highData.add(data.high)
      lowData.add(data.low)
      openData.add(data.open)
      closeData.add(data.close)
    }
    chart.addSeries("Changes", openData, highData, lowData, closeData)
    sw.displayChart()
  }

}
