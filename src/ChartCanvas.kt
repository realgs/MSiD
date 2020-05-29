import org.knowm.xchart.*

class ChartCanvas(title: String, dataset: List<ChartData>){

  private val chart =
    OHLCChartBuilder().width(600).height(400).title(title)
      .xAxisTitle("Time").build()

  private val histogram: CategoryChart = CategoryChartBuilder().width(600).height(400).title(title).xAxisTitle("Time").build()

  private val swo: SwingWrapper<OHLCChart> = SwingWrapper<OHLCChart>(chart)
  private val swh: SwingWrapper<CategoryChart> = SwingWrapper<CategoryChart>(histogram)

  init{
    chart.addSeries("Changes", dataset.map{ it.open }, dataset.map{ it.high }, dataset.map { it.low }, dataset.map { it.close })
    histogram.addSeries("Volume", (1..dataset.size).toList(), dataset.map { it.volume })
    swo.displayChart()
    swh.displayChart()
  }

}
