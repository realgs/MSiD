import java.util.ArrayList;
import java.util.Date;
import org.jfree.data.xy.DefaultHighLowDataset;

public class DatasetCreator 
{
	Date [] date;
    double[] high;
    double[] low;
    double[] open;
    double[] close;
    double[] volume;
	
    public DatasetCreator(ArrayList<Record> dane)
    {
    	int size = dane.size();
    	date = new Date[size];
    	high = new double[size];
        low = new double[size];
        open = new double[size];
        close = new double[size];
        volume = new double[size];
    	
    	for(int i=0; i<size; i++)
    	{
    		date[i] = dane.get(i).data;
    		high[i] = dane.get(i).high;
    		low[i] = dane.get(i).low;
    		open[i] = dane.get(i).open;
    		close[i] = dane.get(i).close;
    		volume[i] = dane.get(i).volume;
    	}
    }
   
	public DefaultHighLowDataset createDataset()
	{
		return new DefaultHighLowDataset("Seria danych", date, high, low, open, close, volume);
	}
}
