
public class Daily {

	private String date;
	private double volume, open, max, min, close;
	
	public Daily(String date, double volume, double open, double max, double min, double close)
	{
		this.date = date;
		this.volume = volume;
		this.open = open;
		this.max = max;
		this.min = min;
		this.close = close;
	}
	
	public String getDate() {
		return date;
	}

	public double getVolume() {
		return volume;
	}

	public double getOpen() {
		return open;
	}

	public double getMax() {
		return max;
	}

	public double getMin() {
		return min;
	}

	public double getClose() {
		return close;
	}
	
	public void combine(Daily other) {
		
		if(date.equals(other.date)) {
			
			volume += other.volume;
			open += other.open;
			max += other.max;
			min += other.min;
			close += other.close;
		}
		else throw new IllegalArgumentException("Notowania musza dotyczyc tego samego dnia!");
	}

	public void getAvg(int size) {
		volume /= size; 
		open /= size;
		max /= size;
		min /= size;
		close /= size;
	}
	
	public String toCSV() {
		return String.format("%s;%.2f;%.2f;%.2f;%.2f;%.2f", date, volume, open, max, min, close);
	}
	
	@Override
	public String toString() { 
		return String.format("%-14s Wolumen: %-10.2f Otwarcie: %-10.2f Max: %-10.2f Min: %-10.2f Zamkniecie: %-10.2f", date, volume, open, max, min, close);
	}
	
	
}
