import java.io.BufferedWriter;
import java.io.FileWriter;
import java.util.ArrayList;

import javax.swing.SingleSelectionModel;

public class Main 
{
	static String from = "2020-01-01", to = "2020-06-06", sim_target = "2020-12-31";
	
	public static ArrayList<Record> avgFromSim(int simCounter, String filename) throws Exception
	{
		ArrayList<Record> history = new ArrayList<Record>(), averagePred = new ArrayList<Record>();
		Simulator sim = new Simulator("cexio_btcusd_daily.csv", from, to);
		history.addAll(sim.history);
		sim.makePrediction(sim_target);

		averagePred.addAll(sim.prediction);
		
		for(int i=1; i<simCounter; i++)
		{
			sim.makePrediction(sim_target);
			for(int j=0; j<averagePred.size(); j++)
			{
				averagePred.get(j).close+=sim.prediction.get(j).close;
				averagePred.get(j).high+=sim.prediction.get(j).high;
				averagePred.get(j).low+=sim.prediction.get(j).low;
				averagePred.get(j).open+=sim.prediction.get(j).open;
				averagePred.get(j).volume+=sim.prediction.get(j).volume;
			}
		}
		
		for(Record r : averagePred)
		{
			r.close /= simCounter;
			r.high /= simCounter;
			r.low /= simCounter;
			r.open /= simCounter;
			r.volume /= simCounter;
		}
		history.addAll(averagePred);
		
		BufferedWriter writer = new BufferedWriter(new FileWriter(filename));
		
		for(Record r : averagePred)
		{
			writer.write(r.toSeparatedFile());
			writer.newLine();
		}
		writer.close();
		return history;
	}
	
	public static void singleSim() throws Exception
	{
		Simulator sim = new Simulator("cexio_btcusd_daily.csv", from, to);
		sim.showParameters();
		sim.makePrediction(sim_target);
		sim.showPrediction();
		
		sim.saveSim("btdusd_"+from+"_to_"+to+"_predicted_to_"+sim_target+".csv");
		
		ArrayList<Record> plotData = new ArrayList<>();
		plotData.addAll(sim.history);
		plotData.addAll(sim.prediction);
				
		CandlestickChart wykres = new CandlestickChart("BTC/USD", plotData);
		wykres.showChart();
	}
	
	public static void main(String[] args) throws Exception 
	{	
//		ArrayList<Record> avg = avgFromSim(100,"100btdusd_"+from+"_to_"+to+"_predicted_to_"+sim_target+".csv");
//		CandlestickChart wykres = new CandlestickChart("BTC/USD", avg);
//		wykres.showChart();
		
		singleSim();
	}
}
