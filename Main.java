import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class Main {
	
	public static void toCSV(String filename, ArrayList<Daily> generated) {
		
		try {
			BufferedWriter buffer = new BufferedWriter(new FileWriter(filename));
			for(int i=0; i<generated.size(); i++)
			{
				buffer.write(generated.get(i).toCSV());
				buffer.newLine();
			}
			buffer.close();
		} 
		catch (IOException e) {
			e.printStackTrace();
		}
		
	}
	
	public static void simulation(String date, String learnFrom, String learnTo, int numberOfSims, boolean printOutput) throws Exception {
		
		if(numberOfSims > 0)
		{
			Simulator simulator = new Simulator("btc_history.csv", learnFrom, learnTo);
			simulator.showModificators();
			System.out.println("Symulacja nr"+1);
			simulator.simulate(date, printOutput);
			
			ArrayList<Daily> predictions = simulator.getGenerated(); 
			double predSize = predictions.size();
			
			for(int i=1; i<numberOfSims; i++)
			{
				System.out.println("\nSymulacja nr"+(i+1));
				simulator.simulate(date, printOutput);
				for(int j=1; j<=predSize; j++)
				{
					predictions.get(j-1).combine(simulator.getGenerated().get(j-1));
				}
			}
			
			for(Daily day : predictions)
			{
				day.getAvg(numberOfSims);
			}
			toCSV("sim_to_"+date+"_"+numberOfSims+"based_"+learnFrom+"_"+learnTo+".csv", predictions);
		}
		else throw new IllegalArgumentException("Liczba symulacji musi byc wieksza od 0!");
	}
	
	
	public static void main(String[] args) throws Exception {
		
		simulation("2020-08-31", "2020-06-01", "2020-01-01", 1, true);
		simulation("2020-08-31", "2020-06-01", "2020-01-01", 100, true);
	}

}
