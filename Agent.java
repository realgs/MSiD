import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;

/*
	Agent podejmuje decyzje w oparciu o wskazniki dlugoterminowe, przyjmuj�c przekazane
	kursy jako kursy zamkni�cia danego dnia, dla maksymalizacji efektywno�ci cz�sotliwo��
	podejmowania decyzji, powinna zosta� dopasowana do danych z pliku CSV 
	(w tym przypadku najlepiej powinno dzia�a� podejmowanie decyzji z dnia na dzie�)
*/

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
			return String.format("%-15s| kurs zamkni�cia: %-12.2f| zmiana: %7.2f", date, closeValue, change);
		}
	}
	
	ArrayList<Record> dane;
	Orderbook book;
	boolean worth=false;
	double lastAvgMaRatio=0.0;
	double currentAvgMaRatio=0.0;
	
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
	
	public double calcMovingAverage(int modifyDate, int shortRange, int longRange, double...vals)
	{
		lastAvgMaRatio = currentAvgMaRatio;
		
		if(modifyDate+shortRange>dane.size() || modifyDate+longRange>dane.size())
		{
			System.out.println("Podany zakres nie jest przechowywany");
			return -1;
		}
		else
		{
			double shortMA=0.0, longMA=0.0;
			
			for(int i=0; i<vals.length; i++)
			{
				shortMA+=vals[i];
				longMA+=vals[i];
			}
			
			int i=modifyDate;
			for(; i<modifyDate+shortRange-vals.length; i++)
			{
				shortMA+=dane.get(i).closeValue;
				longMA+=dane.get(i).closeValue;
			}
			
			for(; i<longRange; i++)
			{
				longMA+=dane.get(i).closeValue;
			}
			
			shortMA/=(double)shortRange;
			longMA/=(double)longRange;
			
			if(shortMA>longMA) worth=true;
			System.out.println("------------------------------------");
			System.out.println("Moving Avg"+shortRange+":\t"+ shortMA + "\nMoving Avg"+longRange+":\t" +longMA);
			System.out.println("------------------------------------");
			
			currentAvgMaRatio = (shortMA+longMA)/2;
			System.out.println("Stosunek �rednich krocz�cych:" + currentAvgMaRatio);
			
			return currentAvgMaRatio;
		}
		
	}
	
	/*
		Funkcja zwraca podejmowan� decyzj� (1: kupno, 0: oczekiwanie, -1: sprzedaz)
		Zmienna modifyDate pozwala manipulowa� okresem analizowanych danych 
		np. je�eli chcemy analizowa� dane (wstecz) pocz�wszy od dzisiaj 
		modifyDate powinno przyj�� warto�� 0, je�eli chcemy zacz�� analiz� tydzie� wstecz
		modifyDate powinno przyj�� warto�� 7
	*/
	
	public int makeDecision(Orderbook book, int shortRange, int longRange, int modifyDate) throws Exception 
	{
		book.update(1);
		calcMovingAverage(modifyDate, shortRange, longRange, book.buy.get(0).price);
		
		if(lastAvgMaRatio!=0 && currentAvgMaRatio<lastAvgMaRatio && worth)
		{
			System.out.println("DECYZJA KUP");
			return 1;
		}
		else if (lastAvgMaRatio!=0 && currentAvgMaRatio>lastAvgMaRatio)
		{
			System.out.println("DECYZJA SPRZEDAJ");
			return -1;
		}
		else
		{
			System.out.println("DECYZJA CZEKAJ");
			return 0;
		}
	}
	
}
