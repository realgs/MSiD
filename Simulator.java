import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

public class Simulator 
{
	ArrayList <Record> history;
	ArrayList <Record> prediction;
	double highChangeVal=0;
	double lowChangeVal=0;
	double closeGrowProb=0, closeChangeVal=0;
	double volGrowProb=0, volChangeVal=0;
	
	double average=0, median, stdDeviation=0;
	
	public Simulator(String sourceFile, String fromDate, String toDate) throws Exception
	{
		LocalDate from=LocalDate.parse(fromDate), to=LocalDate.parse(toDate);
		if(from.isAfter(to)) throw new IllegalArgumentException("Zly zakres dat!");
		if(from.isBefore(LocalDate.parse("2015-02-08")) || from.isAfter(LocalDate.parse("2020-06-06")) || to.isAfter(LocalDate.parse("2020-06-06"))) throw new IllegalArgumentException("Brak danych!");
		
		history = new ArrayList<>();
		prediction = new ArrayList<>();
		
		BufferedReader reader = new BufferedReader(new FileReader(sourceFile));
		String line=""; String [] input;
		
		while((line=reader.readLine())!=null)
		{
			input = line.split(";");
			
			if(!LocalDate.parse(input[0]).isAfter(to))
			{
				if(LocalDate.parse(input[0]).isBefore(from)) break;
				
				history.add(new Record(input[0], Double.parseDouble(input[1]),Double.parseDouble(input[2]), 
						Double.parseDouble(input[3]), Double.parseDouble(input[4]), Double.parseDouble(input[5])));
			}
		}
		
		reader.close();
		getParameters();
	}
	
	public void getParameters()
	{
		int historySize = history.size();
		
		for(int i=0; i<historySize-1; i++)
		{
			if(history.get(i).close > history.get(i+1).close) closeGrowProb++;
			if(history.get(i).volume > history.get(i+1).volume) volGrowProb++;
			
			highChangeVal += (history.get(i).high - Math.max(history.get(i).open, history.get(i).close));
			lowChangeVal += (Math.min(history.get(i).open, history.get(i).close) - history.get(i).low);
			closeChangeVal += (Math.abs(history.get(i).close - history.get(i+1).close));
			volChangeVal += (Math.abs(history.get(i).volume - history.get(i+1).volume));
		}
		highChangeVal += Math.abs(history.get(historySize-1).high - history.get(historySize-1).open);
		lowChangeVal += Math.abs(history.get(historySize-1).low - history.get(historySize-1).open);
		
		closeGrowProb /= (historySize-1);
		closeChangeVal /= (historySize-1);
		
		volGrowProb /= (historySize-1);
		volChangeVal /= (historySize-1);
		
		highChangeVal /= historySize;
		lowChangeVal /= historySize;
	}
	
	public String calcStats()
	{
		average=0; median=0; stdDeviation=0;
		
		int predicted = prediction.size();
		double [] closePrices = new double[predicted];
		
		for(int i=0; i<predicted; i++)
		{
			average += prediction.get(i).close;
			closePrices[i] = prediction.get(i).close;
		}
		
		Arrays.sort(closePrices);
		if(predicted%2==0)
		{
			median = (closePrices[predicted/2-1] + closePrices[predicted/2])/2.0;
		}
		else
		{
			median = prediction.get(predicted/2).close;
		}
		
		average/=prediction.size();
		
		for (int i = 0; i < predicted; i++) {
		    stdDeviation += (prediction.get(i).close - average) * (prediction.get(i).close - average);
		}
		stdDeviation /= predicted;
		stdDeviation = Math.sqrt(stdDeviation);
		
		String text = String.format("\nSredni kurs %.2f\nMediana: %.2f\nOdcylenie standardowe: %.2f", average, median, stdDeviation);
		System.out.println(text);
		
		return text;
	}
	
	public Record predict(Record previous) 
	{
		String data;
		double high, low, open, close, volume;
		Random r = new Random();
		
		data = previous.data.toInstant().atZone(ZoneId.systemDefault()).toLocalDate().plusDays(1).toString();
		open = previous.close;
		
		double closeDifference = r.nextGaussian()*closeChangeVal;
		if(r.nextDouble()<=closeGrowProb)
		{
			close = previous.close + closeDifference;
		}
		else
		{
			close = previous.close - closeDifference;
		}
		
		high = Math.max(open, close) + Math.abs(r.nextGaussian()*lowChangeVal);
		low = Math.min(open, close) - Math.abs(r.nextGaussian()*lowChangeVal);
		
		double volumeDifference = r.nextGaussian()*0.5*volChangeVal;
		if(r.nextDouble()<=volGrowProb)
		{
			volume = previous.volume + volumeDifference;
		}
		else
		{
			volume = (Math.max(0, previous.volume - volumeDifference));
		}
		
		return new Record(data, high, low, open, close, volume);
	}
	
	public ArrayList<Record> makePrediction(String date) throws Exception
	{
		LocalDate lastLearnt = history.get(0).data.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
		if(LocalDate.parse(date).isAfter(lastLearnt))
		{
			prediction = new ArrayList<Record>();
			prediction.add(predict(history.get(0)));
			int daysToPredict = (int)ChronoUnit.DAYS.between(lastLearnt, LocalDate.parse(date));
			
			for(int i=1; i<daysToPredict; i++)
			{
				prediction.add(predict(prediction.get(i-1)));
			}
			
		}
		else throw new IllegalAccessException("Przewidywania musza dotyczy przyszlosci");
		
		return prediction;
	}
	
	
	public void showHistory()
	{
		for(Record r : history)
		{
			System.out.println(r);
		}
	}
	
	public void showPrediction()
	{
		for(Record r : prediction)
		{
			System.out.println(r);
		}
	}
	
	public void showParameters()
	{
		System.out.println(String.format("PARAMETRY SYMULACJI:\nSrednia zmiana max: %.2f"
							+ "\nSrednia zmiana min: %.2f\nSzansa wzrostu zamkniecia: %.2f\nSrednia zmiana zamkniecia: %.2f"
							+ "\nSzansa wzrostu wolumenu: %.2f\nSrednia zmiana wolumenu: %.2f", 
							highChangeVal,lowChangeVal,closeGrowProb,closeChangeVal,volGrowProb,volChangeVal));
	}
	
	public void saveSim(String filename) throws Exception
	{
		BufferedWriter writer = new BufferedWriter(new FileWriter(filename));
		
		writer.write(String.format("PARAMETRY SYMULACJI:\nSrednia zmiana max: %.2f"
				+ "\nSrednia zmiana min: %.2f\nSzansa wzrostu zamkniecia: %.2f\nSrednia zmiana zamkniecia: %.2f"
				+ "\nSzansa wzrostu wolumenu: %.2f\nSrednia zmiana wolumenu: %.2f", 
				highChangeVal,lowChangeVal,closeGrowProb,closeChangeVal,volGrowProb,volChangeVal));
		writer.newLine();
		
		for(Record r : history)
		{
			writer.write(r.toSeparatedFile());
			writer.newLine();
		}
		
		for(Record r : prediction)
		{
			writer.write(r.toSeparatedFile());
			writer.newLine();
		}
		writer.newLine();
		writer.write(calcStats());
		
		writer.close();
	}
}
