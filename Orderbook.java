import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;

abstract public class Orderbook 
{
	URL source;
	ArrayList <Offer> buy;
	ArrayList <Offer> sell;
	
	public Orderbook(URL source) throws IOException 
	{
		buy = new ArrayList<Offer>();
		sell = new ArrayList<Offer>();
		this.source = source;

	}
	
	public Orderbook(ArrayList<Offer> buy, ArrayList<Offer> sell, URL source) throws IOException
	{
		this.buy = buy;
		this.sell = sell;
		this.source = source;
	}
	
	public double buySellDiff()
	{
		System.out.println(String.format("|BUY: %-15.2f|SELL: %-15.2f|", buy.get(0).price, sell.get(0).price));
		return ( (sell.get(0).price - buy.get(0).price)/buy.get(0).price )*100;
	}
	
	public double calcDiff() throws IOException
	{
		double diff = ((sell.get(0).price - buy.get(0).price)/buy.get(0).price )*100;
		System.out.println(String.format("|BUY: %-15.2f|SELL: %-15.2f|\nRó¿nica:%10.6f%%", buy.get(0).price, sell.get(0).price, diff));
		return diff;
	}
	
	public void printOrderbook()
	{
		for(Offer o : buy)
		{
			System.out.println(o);
		}
		
		System.out.println("\n___________________________________________________\n");
		
		for(Offer o : sell)
		{
			System.out.println(o);
		}
		System.out.println();
	}
	
	abstract void update(int limit) throws IOException;

	public void inspect(long interval) throws IOException, InterruptedException
	{
		while(true)
		{
			update(1);
			calcDiff();
			Thread.sleep(interval);
		}
	}
	
	
}
