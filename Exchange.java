import java.net.URL;
import java.util.ArrayList;

public class Exchange 
{
	private JSONParser parser;
	private String name, currency1, currency2;
	private ArrayList <Offer> bids, asks;
	
	public Exchange(String name, String currency1, String currency2, int quantity) {
		this.name = name;
		this.currency1 = currency1;
		this.currency2 = currency2;
		this.bids = new ArrayList<Offer>();
		this.asks = new ArrayList<Offer>();
		createParser();
		fillData(quantity);
	}
	
	public ArrayList<Offer> getBids() {
		return bids;
	}

	public ArrayList<Offer> getAsks() {
		return asks;
	}
	
	public void printOrderbook() {

		System.out.println("\n------------------------------------------------\n"+ name + " Exchange\t("+currency1+" - "+currency2+")");
		System.out.println("\nBIDS\n------------------------------------------------");
		
		for(Offer bid : bids) {
			System.out.println("BID: " + bid);
		}
		System.out.println("------------------------------------------------\n\nASKS\n------------------------------------------------");
		
		
		for(Offer ask : asks) {
			System.out.println("ASK: " + ask);
		}
		System.out.println("------------------------------------------------");
	}
	
	public void update(int quantity) {
		parser.updateData();
		fillData(quantity);
	}
	
	private void fillData(int quantity) {
		switch(name) {
			case "BitBay":
				bitbayData(quantity);
				break;
			case "CEX.IO":
				cexioData(quantity);
				break;
			case "WhiteBit":
				whitebitData(quantity);
				break;
			case "Ftx":
				ftxData(quantity);
				break;
			default:
				System.out.println("Nie obs³ugiwane Ÿród³o!");
		}
	}

	private void bitbayData(int quantity) {
		
		String [] tab = parser.getData(); 
		int i=0, counter=0;
		
		tab[0]=tab[0].replace("bids", "");

		for(; !tab[i].contains("asks"); i+=2) {
			
			if(counter < quantity) {
				if(bids.size()==counter) bids.add(new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1])));
				else bids.set(counter, new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1])));
				counter++;
			}
		}
		
		counter = 0;
		tab[i]=tab[i].replace("asks", "");
		
		for(; i<tab.length-1; i+=2) {
			
			if(counter < quantity) {
				if(asks.size()==counter) asks.add(new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1])));
				else asks.set(counter, new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1])));
				counter++;
			}
		}
		
		bids.trimToSize(); asks.trimToSize();
	}
	
	private void cexioData(int quantity) {
		
		String [] tab = parser.getData(); 
		int i=1, counter=0;
		
		tab[1]=tab[1].replace("bids", "");	
		
		for(; !tab[i].contains("asks"); i+=2) {
			
			if(counter < quantity) {
				if(bids.size()==counter) bids.add(new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1])));
				else bids.set(counter, new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1])));
				counter++;
			}
		}
		
		counter = 0;
		tab[i]=tab[i].replace("asks", "");
		
		for(; !tab[i].contains("pair"); i+=2) {
			
			if(counter < quantity) {
				if(asks.size()==counter) asks.add(new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1])));
				else asks.set(counter, new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1])));
				counter++;
			}
		}
		
		bids.trimToSize(); asks.trimToSize();
	}
	
	private void whitebitData(int quantity) {
		
		String [] tab = parser.getData(); 
		int i=0, counter=0;
		
		tab[0]=tab[0].replace("asks", "");
		
		for(; !tab[i].contains("bids"); i+=2) {
			
			if(counter < quantity) {
				if(asks.size()==counter) asks.add(new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1])));
				else asks.set(counter, new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1])));
				counter++;
			}
		}
		
		counter = 0;
		tab[i]=tab[i].replace("bids", "");
		
		for(; i<tab.length-1; i+=2) {
			
			if(counter < quantity) {
				if(bids.size()==counter) bids.add(new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1])));
				else bids.set(counter, new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1])));
				counter++;
			}
		}
		
		bids.trimToSize(); asks.trimToSize();
	}
	
	private void ftxData(int quantity) {
		
		String [] tab = parser.getData(); 
		int i=0, counter=0;
		
		tab[0]=tab[0].replace("resultasks", "");	
		
		
		for(; !tab[i].contains("bids"); i+=2) {
			
			if(counter < quantity) {
				if(asks.size()==counter) asks.add(new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1])));
				else asks.set(counter, new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1])));
				counter++;
			}
		}
		
		counter = 0;
		tab[i]=tab[i].replace("bids", "");
		
		for(; !tab[i].contains("suc"); i+=2) {
			
			if(counter < quantity) {
				if(bids.size()==counter) bids.add(new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1])));
				else bids.set(counter, new Offer(Double.parseDouble(tab[i]),Double.parseDouble(tab[i+1])));
				counter++;
			}
		}
		
		bids.trimToSize(); asks.trimToSize();
	}

	private void createParser()
	{
		String address="";
		switch(name) {
		case "BitBay":
			address=String.format("https://bitbay.net/API/Public/%s%s/orderbook.json", currency1, currency2);
			break;
		case "CEX.IO":
			address=String.format("https://cex.io/api/order_book/%s/%s/", currency1, currency2);
			break;
		case "WhiteBit":
			address=String.format("https://whitebit.com/api/v1/public/depth/result?market=%s_%s&limit=10", currency1, currency2);
			break;
		case "Ftx":
			address=String.format("https://ftx.com/api//markets/%s_%s/orderbook", currency1, currency2);
			break;
		default:
			System.out.println("Nie obs³ugiwane Ÿród³o!");
		}
		
		try {
			if(address!="") this.parser = new JSONParser(new URL(address));
		}
		catch (Exception e){
			e.printStackTrace();
		}
	}
}
