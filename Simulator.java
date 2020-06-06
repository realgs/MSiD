import java.io.BufferedReader;
import java.io.FileReader;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;


public class Simulator {
	
	private Daily current = null;
	private ArrayList<Daily> notowania;
	private ArrayList<Daily> generated;
	private int dataSize;
	private double volumeModificator;
	private double closeValueMod, closeDistrFunction;
	private double minModificator;
	private double maxModificator;
	
	public Simulator(String csvFile, String fromDate, String toDate) throws Exception {
		notowania = new ArrayList<>();
		generated = new ArrayList<>();
		dataSize=0;
		LocalDate today=LocalDate.now().plusDays(1), since = LocalDate.parse(fromDate).plusDays(1);
		
		if(today.isBefore(since)) throw new IllegalArgumentException("Podana data musi byc wczesniejsza lub rowna dzisiejszej!");
		else if (since.isBefore(LocalDate.of(2016, 1, 1))) throw new IllegalArgumentException("Podana data musi byæ pozniejsza ni¿ 1 stycznia 2016r.");
		else {
			
			try {
				BufferedReader buffer = new BufferedReader(new FileReader(csvFile));
				String [] dane; String line="";
				
				while( (line=buffer.readLine()) != null) {
						
						dane = line.replaceAll("[^0-9.;-]", "").split(";");
						
						if(current==null) current = new Daily(LocalDate.now().toString(), Double.parseDouble(dane[1]), Double.parseDouble(dane[2]), 
											Double.parseDouble(dane[3]), Double.parseDouble(dane[4]), Double.parseDouble(dane[5]));
											
						if(LocalDate.parse(dane[0]).isBefore(since)) {
							notowania.add(new Daily(dane[0], Double.parseDouble(dane[1]), Double.parseDouble(dane[2]), 
													Double.parseDouble(dane[3]), Double.parseDouble(dane[4]), Double.parseDouble(dane[5])));
							dataSize++;
							
							if(line.contains(toDate)) break;
						}
				}
				
				buffer.close();
			} 
			catch (Exception e) {
				System.out.println("Nie mo¿na odnalezc pliku!");
			}
		}
		calcModificators();
	}

	public ArrayList<Daily> getNotowania() {
		return notowania;
	}
	
	public void showModificators()
	{
		System.out.println("\nPARAMETRY SYMULACJI:");
		System.out.println("VolumeModificator: "+volumeModificator);
		System.out.println("CloseValueMod: "+closeValueMod + "\tcloseDistrFunction: " + closeDistrFunction);
		System.out.println("MinModificator: "+minModificator);
		System.out.println("MaxModificator: "+maxModificator + "\n");
	}
	
	public void simulate(String toDate, boolean printOutput)
	{
		LocalDate target = LocalDate.parse(toDate);
		if(LocalDate.now().plusDays(1).isAfter(target)) throw new IllegalArgumentException("Data do symulacji musi byc w przyszlosci!");
		else
		{
			generated = new ArrayList<Daily>();
			generated.add(makePrediction(current));
			int daystoTarget = (int)ChronoUnit.DAYS.between(LocalDate.now(), target);
			
			for(int i=1; i<daystoTarget; i++)
			{
				generated.add(makePrediction(generated.get(i-1)));
			}
		}
		if(printOutput) printSimulated();
		calcStatistics();
	}
	
	public void printSimulated()
	{
		if(generated.isEmpty()) throw new IllegalStateException("Aby wyswietlic statystyki musisz najpierw przeprowadzic statystki!");
		else
		{
			for(int i=0; i<generated.size(); i++)
			{
				System.out.println(generated.get(i));
			}
		}
	}
	
	public void calcStatistics()
	{
		if(generated.isEmpty()) throw new IllegalStateException("Aby wyswietlic statystyki musisz najpierw przeprowadzic statystki!");
		else
		{
			double average=0.0, median, variance=0.0, deviation; 
			int genSize = generated.size();
			double [] closePrices = new double[genSize];
			
			for(int i=0; i<genSize; i++)
			{
				average += generated.get(i).getClose();
				closePrices[i] = generated.get(i).getClose();
			}
			
			Arrays.sort(closePrices);
			if(genSize%2==0)
			{
				median = (closePrices[genSize/2-1] + closePrices[genSize/2])/2.0;
			}
			else
			{
				median = generated.get(genSize/2).getClose();
			}
			
			average/=generated.size();
			
			for (int i = 0; i < genSize; i++) {
			    variance += (generated.get(i).getClose() - average) * (generated.get(i).getClose() - average);
			}
			variance /= genSize;
			deviation = Math.sqrt(variance);
			
			System.out.println(String.format("\nSredni kurs\t\t%10.3f", average));
			System.out.println(String.format("Mediana:\t\t%10.3f", median));
			System.out.println(String.format("Wariancja:\t\t%10.3f", variance));
			System.out.println(String.format("Odcylenie standardowe:\t%10.3f", deviation));
			
		}
	}
	
	public ArrayList<Daily> getGenerated() {
		return generated;
	}
	
	private void calcModificators()
	{
		double volMod=0.0, closeVal=0.0, closeDistr=0, minMod=0.0, maxMod=0.0;
		
		for(int i=0; i<dataSize-1; i++)
		{
			if(notowania.get(i).getClose() > notowania.get(i+1).getClose()) closeDistr++;
			volMod += Math.abs(notowania.get(i).getVolume() - notowania.get(i+1).getVolume());
			closeVal += Math.abs(notowania.get(i).getClose() - notowania.get(i+1).getClose());
			minMod += notowania.get(i).getOpen() - notowania.get(i).getMin();
			maxMod += notowania.get(i).getMax() - notowania.get(i).getOpen();
		}
		minMod += notowania.get(dataSize-1).getOpen() - notowania.get(dataSize-1).getMin();
		maxMod += notowania.get(dataSize-1).getMax() - notowania.get(dataSize-1).getOpen();
		
		volumeModificator = volMod/(dataSize-1);
		closeValueMod = closeVal/(dataSize-1);
		closeDistrFunction = closeDistr/(dataSize-1);
		minModificator = minMod/dataSize;
		maxModificator = maxMod/dataSize;
	}
	
	private Daily makePrediction(Daily previous)
	{
		Random rand = new Random();
		String date; 
		double volume, open, max, min, close;
		
		date = LocalDate.parse(previous.getDate()).plusDays(1).toString();
		volume = Math.max(0, previous.getVolume() + ((double)Math.round((rand.nextGaussian()+0.072)*volumeModificator*100)/100));
		open = previous.getClose();
		max = Math.max(0, open + ((double)Math.round(Math.abs(rand.nextGaussian()*0.7)*maxModificator*100)/100));
		min = Math.max(0, open - ((double)Math.round(Math.abs(rand.nextGaussian()*0.7)*maxModificator*100)/100));
		
		double tendention = rand.nextDouble(), change = ((double)Math.round(Math.abs(rand.nextGaussian()*0.8)*closeValueMod*100)/100);
		
		if(tendention<=closeDistrFunction)
		{
			close = Math.max(0, previous.getClose() + change);
		}
		else
		{
			close = Math.max(0, previous.getClose() - change);
		}
		
		return new Daily(date, volume, open, max, min, close);
	}
	
}
