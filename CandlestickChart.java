import java.util.ArrayList;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.xy.DefaultHighLowDataset;
import org.jfree.ui.ApplicationFrame;
import org.jfree.ui.RefineryUtilities;

public class CandlestickChart extends ApplicationFrame 
{
	private static final long serialVersionUID = 1L;
	ArrayList<Record> dane;
	String title;

	public CandlestickChart(String title, ArrayList<Record> data) 
	{
        super(title);
        this.title = title;
        this.dane = data;
        DatasetCreator creator = new DatasetCreator(dane);
        final DefaultHighLowDataset dataset = creator.createDataset();
        final JFreeChart chart = createChart(dataset);
        final ChartPanel chartPanel = new ChartPanel(chart);
        
        chart.getXYPlot().setOrientation(PlotOrientation.VERTICAL);
        //chart.getXYPlot().getRangeAxis().setRange(3000,14000);
        chartPanel.setPreferredSize(new java.awt.Dimension(500, 270));
        setContentPane(chartPanel);

    }

    private JFreeChart createChart(DefaultHighLowDataset dataset) 
    {
        final JFreeChart chart = ChartFactory.createCandlestickChart("Wykres BTC/USD", "Data", "Cena [USD]", dataset, true);
        return chart;        
    }
    
    public void showChart()
    {
    	final CandlestickChart chart = new CandlestickChart(title, dane);
    	chart.pack();
        RefineryUtilities.centerFrameOnScreen(chart);
        chart.setVisible(true);
    }
}