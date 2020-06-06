import java.util.ArrayList;

public class Main 
{
	public static void main(String[] args) throws Exception 
	{
		String from = "2020-01-01", to = "2020-06-06", sim_target = "2020-12-31";
		Simulator sim = new Simulator("cexio_btcusd_daily.csv", from, to);
		sim.showParameters();
		sim.makePrediction(sim_target);
		sim.showPrediction();
		sim.calcStats();
		sim.saveSim("btdusd_"+from+"_to_"+to+"_predicted_to_"+sim_target+".csv");
		
		ArrayList<Record> plotData = new ArrayList<>();
		plotData.addAll(sim.history);
		plotData.addAll(sim.prediction);
				
		CandlestickChart wykres = new CandlestickChart("BTC/USD", plotData);
		wykres.showChart();
		
	}
}
