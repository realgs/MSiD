import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;

public class JSONParser 
{
	private URL source;
	private ArrayList<Offer> bids;
	private ArrayList<Offer> asks;
	
	public JSONParser(URL source) {
		this.source = source;
		bids = new ArrayList<Offer>();
		asks = new ArrayList<Offer>();
	}
	
	public ArrayList<Offer> getBids() {
		return bids;
	}

	public void setBids(ArrayList<Offer> bids) {
		this.bids = bids;
	}

	public ArrayList<Offer> getAsks() {
		return asks;
	}

	public void setAsks(ArrayList<Offer> asks) {
		this.asks = asks;
	}

	public void getData() throws IOException {
		
		String tab[]; int i=0;  
		bids = new ArrayList<Offer>();
		asks = new ArrayList<Offer>();
		
		URLConnection connection = source.openConnection();
		connection.connect();
		
		BufferedReader buffer = new BufferedReader(new InputStreamReader(connection.getInputStream()));
		
		tab = buffer.readLine().replaceAll("[:\\[\\]\\{\\}]", "").split(",");
		
		tab[0]=tab[0].replace("\"bids\"", "");

		for(; !tab[i].contains("asks"); i+=2) {
			Offer create = new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1]));
			bids.add(create);
		}
		
		tab[i]=tab[i].replace("\"asks\"", "");
		
		
		for(; i<tab.length-1; i+=2) {
			Offer create = new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1]));
			asks.add(create);
		}
	}
	
}
