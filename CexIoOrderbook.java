import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;

public class CexIoOrderbook extends Orderbook
{
	public CexIoOrderbook(String currency1, String currency2) throws IOException 
	{
		super(new URL("https://cex.io/api/order_book/"+currency1+"/"+currency2+"/"));
	}
	
	@Override
	void update(int limit) throws IOException 
	{
		String tab[];
		buy = new ArrayList<Offer>(); sell = new ArrayList<Offer>();
		int i=1, counter=0;
		
		//long start = System.currentTimeMillis();
		
		URLConnection connection = source.openConnection();
		connection.addRequestProperty("User-Agent", "Mozilla");
		connection.connect();
		
		BufferedReader buffer = new BufferedReader(new InputStreamReader(connection.getInputStream()));
		
		//System.out.println("CexIo: "+ (System.currentTimeMillis()-start));
		
		
		tab = buffer.readLine().replaceAll("[:\\[\\]\\{\\}]", "").split(",");

		tab[1]=tab[1].replace("\"bids\"", "");	

		for(; !tab[i].contains("asks"); i+=2)
		{
			if(counter < limit)
			{
				Offer temp = new Offer(true,Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1]));
				buy.add(temp);
				counter++;
			}
		}
		
		counter = 0;
		tab[i]=tab[i].replace("\"asks\"", "");
		
		for(; !tab[i].contains("pair"); i+=2)
		{
			if(counter < limit)
			{
				Offer temp = new Offer(false,Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1]));
				sell.add(temp);
				counter++;
			}
		}
		
		buy.trimToSize();
		sell.trimToSize();
	}

}