import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.FileReader;
import java.time.LocalDate;

public class DecisionMaker 
{
	private ArrayList<Quotation> historical;
	private double expAverage;

	public class Quotation {
		
		private String date;
		private double close, volume;
		
		public Quotation(String date, double close, double volume) {
			this.date = date;
			this.close = close;
			this.volume = volume;
		}

		public String getDate() {
			return date;
		}

		public double getClose() {
			return close;
		}
		
		public double getVolume() {
			return volume;
		}

		@Override
		public String toString() {
			return String.format("%s kurs: %.2f wolumen: %.2f", date, close, volume);
		}
	}
	
	//tworzenie agenta decyzyjnego w oparciu o dane historyczne i analizowany przedzial czasowy (data w formacie rrrr-mm-dd)
	public DecisionMaker(String csvFile, String dateToAnalyzeFrom) throws Exception {
		historical = new ArrayList<>();
		LocalDate today=LocalDate.now(), since = LocalDate.parse(dateToAnalyzeFrom);
		
		if(today.isBefore(since)) throw new IllegalArgumentException("Podana data musi byæ wczeœniejsza od dzisiejszej!");
		else if (since.isBefore(LocalDate.of(2019, 1, 1))) throw new IllegalArgumentException("Podana data musi byæ póŸniejsza ni¿ 1 stycznia 2020r.");
		else {
			
			try {
				BufferedReader buffer = new BufferedReader(new FileReader(csvFile));
				String [] dane; String line="";
				
				while( (line=buffer.readLine()) != null) {
					
					dane = line.replaceAll("[^0-9.;-]", "").split(";");
					historical.add(new Quotation(dane[0], Double.parseDouble(dane[1]), Double.parseDouble(dane[2])));
					if(line.contains(dateToAnalyzeFrom)) break;
				}
				
				buffer.close();
			} 
			catch (Exception e) {
				System.out.println("Nie mo¿na odnaleŸæ pliku!");
			}
			
			expAverage=exponentialAverage();
		}
		
	}
	
	public ArrayList<Quotation> getHistorical() {
		return historical;
	}
	
	public double getExpAverage() {
		return expAverage;
	}
	
	public int makeDecision(double currentPrice) {
		
		double currentAverage = exponentialAverage(currentPrice);
		
		// jesli wykres sredniej exponencjalnej przecina sie z wykresem kursu waluty od dolu wysylany jest sygnal kupna
		
		if(expAverage<currentPrice && currentPrice <= currentAverage) {
			System.out.println("KUP");
			return 1;
		}
		
		// jesli wykres sredniej exponencjalnej przecina sie z wykresem kursu waluty od gory wysylany jest sygnal sprzedazy
		else if(expAverage>=currentPrice && currentPrice > currentAverage) {
			System.out.println("SPRZEDAJ");
			return -1;
		}
		
		else {
			System.out.println("CZEKAJ");
			return 0;
		}
	}
	
	// wyliczanie sredniej wazonej eksponencjalnej na podstawie danych historycznych
	private double exponentialAverage() {
		
		int N = historical.size();
		double sum = 0, weights = 0;
		
		for(int i=0; i<N-1; i++) {
			
			double factorial = Math.pow(1-(2/(N+1)), i);
			sum += historical.get(i).close*factorial;
			weights += factorial;
		}
		
		return sum/weights;
	}
	
	// wyliczanie sredniej wazonej eksponencjalnej na podstawie danych historycznych oraz obecnego kursu
	public double exponentialAverage(double currentPrice) {
		
		int N = historical.size();
		double sum = currentPrice, weights = 1.0;
		
		for(int i=1; i<N+1; i++) {
			
			double factorial = Math.pow(1-(2/(N+1)), i);
			sum += historical.get(i-1).close*factorial;
			weights += factorial;
		}
		
		return sum/weights;
	}
	
}