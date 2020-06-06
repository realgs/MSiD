import java.time.LocalDate;
import java.time.ZoneId;
import java.util.Date;

public class Record 
{
	Date data;
	double high, low, open, close, volume;
	
	public Record(String date, double high, double low, double open, double close, double volume)
	{
		this.data = Date.from((LocalDate.parse(date).atStartOfDay().atZone(ZoneId.systemDefault()).toInstant()));
		this.high = high;
		this.low = low;
		this.open = open;
		this.close = close;
		this.volume = volume;
	}

	@Override
	public String toString() {
		return String.format("\nData: %-30s\nMax:\t\t%10.2f\nMin:\t\t%10.2f\nOtwarcie:\t%10.2f\nZamkniecie:\t%10.2f\nWolumen:\t%10.2f", data, high, low, open, close, volume);
	}
	
	public String toSeparatedFile()
	{
		return String.format("%s;%.2f;%.2f;%.2f;%.2f;%.2f;", 
				data.toInstant().atZone(ZoneId.systemDefault()).toLocalDate().toString(), 
				high, low, open, close, volume);
	}
	
}
