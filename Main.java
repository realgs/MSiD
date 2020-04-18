import java.util.ArrayList;
import java.net.URL;
import java.io.IOException;

public class Main 
{
	static ArrayList <Offer> bids;
	static ArrayList <Offer> asks;

	private static void printOrderbook(URL source) throws IOException {
		
		JSONParser parser = new JSONParser(source);
		parser.getData();
		bids = parser.getBids();
		asks = parser.getAsks();
		
		System.out.println("BIDS\n------------------------------------------------");
		
		for(Offer bid : bids)
		{
			System.out.println("BID: " + bid);
		}
		System.out.println("------------------------------------------------\n\nASKS\n------------------------------------------------");
		
		
		for(Offer ask : asks)
		{
			System.out.println("ASK: " + ask);
		}
		System.out.println("------------------------------------------------");
	}
	
	private static double calcDiff() {
		System.out.print("KUPNO: " + bids.get(0).getPrice() + "\t SPRZEDAZ: "+ asks.get(0).getPrice());
		return ( (asks.get(0).getPrice() - bids.get(0).getPrice())/bids.get(0).getPrice() )*100;
	}

	private static void inspectDiff(URL source) throws IOException, InterruptedException {
		
		JSONParser parser = new JSONParser(source);
		
		while(true) {
			parser.getData();
			bids = parser.getBids();
			asks = parser.getAsks();
			System.out.println("\tROZNICA: " + calcDiff() + "%");
			Thread.sleep(5000);
		}
		
	}

    public static void main(String[] args) throws Exception {
    	
    	URL bitbay = new URL("https://bitbay.net/API/Public/BTC/orderbook.json");
    	
    	printOrderbook(bitbay);
    	
    	System.out.println();
    	
    	inspectDiff(bitbay);
    	
    }
}