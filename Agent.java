import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;

public class Agent 
{
	public class Record 
	{
		String date;
		double closeValue;
		double change;
		
		public Record(String date, double closeValue, double change)
		{
			this.date = date;
			this.closeValue = closeValue;
			this.change = change;
		}

		@Override
		public String toString() 
		{
			return String.format("%-15s| kurs zamkniêcia: %-12.2f| zmiana: %7.2f", date, closeValue, change);
		}
	}
	
	ArrayList<Record> dane;
	Orderbook book;
	double longTermMA=0.0;
	double shortTermMA=0.0;
	
	public Agent(String dataSource, Orderbook book) throws Exception
	{
		this.book = book;
		
		String tab [], line;
		dane = new ArrayList<Record>();
		
		BufferedReader buffer = new BufferedReader(new FileReader(dataSource));
		
		while( (line=buffer.readLine()) != null)
		{
			line = line.replaceAll("[^0-9.,-]", "");
			tab = line.split(",");
			dane.add(new Record(tab[0], Double.parseDouble(tab[1]), Double.parseDouble(tab[2])));
		}
		buffer.close();
	}
	
	public double calcMA(boolean longTerm, int movingRange, double...vals)
	{
		if(movingRange>dane.size())
		{
			System.out.println("Podany zakres jest za du¿y!");
			return -1;
		}
		else
		{
			double movingAverage=0.0;
			for(int i=0; i<vals.length; i++)
			{
				movingAverage+=vals[i];
			}
			
			for(int i=0; i<movingRange-vals.length; i++)
			{
				movingAverage+=dane.get(0).closeValue;
			}
			
			movingAverage/=(double)movingRange;
			
			if(longTerm)
			{
				longTermMA = movingAverage;
				System.out.println("Long MA" + movingRange + ":\t" + movingAverage);
			}
			else
			{
				shortTermMA = movingAverage;
				System.out.println("Short MA" + movingRange + ":\t" + movingAverage);
			}
			
			return movingAverage;
		}
		
	}
	
	public int makeDecision(Orderbook book, int shortTerm, int longTerm) //Funkcja zwraca podejmowan¹ decyzjê (1: kupno, 0: oczekiwanie, -1: sprzedaz)
	{
		return 1;
	}
	
}
