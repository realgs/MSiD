@SuppressWarnings("unused")
public class Main 
{
	private static String [] currency = {"BTC", "USD", "ETH", "USD", "LTC", "USD", "ETH", "BTC"};
	private static String [] names = {"BitBay", "CEX.IO", "WhiteBit", "Ftx"};
	private static Exchange[][] gieldy = new Exchange[4][4];
	
	private static void arbitrage(Exchange[][] gieldy, Wallet portfel, double tax)
	{
		Offer current, analyze;
		double cost, influence, best;
		
		for(int i=0; i<gieldy[0].length; i++) {
			
			for(int j=0; j<gieldy.length; j++) {
				
				best = 0.0;
				current = gieldy[j][i].getAsks().get(0);
				cost = current.getPrice() * current.getAmmount() * (1+tax);
				
				for(int k=0; k<gieldy.length; k++) {
					
					if(j!=k) {
						
						analyze = gieldy[k][i].getBids().get(0);
						influence = analyze.getPrice() * current.getAmmount() * (1-tax);
						
						if(influence-cost>=0.01) {
							
							System.out.println(String.format("Na gie³dzie %s mo¿na kupiæ %.8f %s za %s po kursie %.2f i sprzedaæ na gie³dzie %s po kursie %.2f zyskuj¹c %.2f%s.", 
							names[j], current.getAmmount(), currency[2*i], currency[2*i+1], current.getPrice(), names[k], analyze.getPrice(), influence-cost, currency[2*i+1]));
											
							if(influence-cost>best) best=influence-cost;
						}
					}
				}
				
				System.out.println();
				if(best>0)portfel.add(currency[2*i+1], best);
			}
		}
	}
	
	private static void zadania1_3(double tax) {
		
		Exchange[][] gieldy = new Exchange[4][4];
		Wallet portfel = new Wallet();
    	
    	for(int i=0; i<gieldy.length; i++) {
    		
    		for(int j=0; j<gieldy[i].length; j++) {
    			
    			gieldy[i][j] = new Exchange(names[i], currency[2*j], currency[2*j+1], 1);
    			//gieldy[i][j].printOrderbook();
    		}
    	}
    	
    	System.out.println();
    	arbitrage(gieldy,portfel,tax);
    	System.out.println(portfel);
	}
	
	private static void zadanie4(int reps, double tax) throws Exception {
		
		Wallet portfel = new Wallet();
		Exchange gielda = new Exchange("CEX.IO", "BTC", "USD", 1);
		
		// agent potrzebuje dwoch parametrów - pliku csv z danymi dotyczacymi kursu zamkniecia i wolumenu oraz daty w formacie rrrr-mm-dd 
		// dla ktorej wylicza srednia wazona eksponencjalna bedacej podstawa podejmowania decyzji (im mniejszy okres tym mniej statyczny jest algorytm)
		DecisionMaker agent = new DecisionMaker("bitcoin_stats.csv", "2020-05-20");
		
		for(int i=0; i<reps; i++) {
			
			if(i>0) gielda.update(1);
			Offer buy=gielda.getAsks().get(0), sell=gielda.getBids().get(0);
			
			// decyzja jest podejmowana w oparciu o cene potencjalnego zakupu 
			int decision = agent.makeDecision(sell.getPrice());
			
			if(decision==1) {
				
				double price = sell.getPrice()*sell.getAmmount()*(1+tax);
				if(portfel.sell("USD", price)) { 
					portfel.add("BTC", sell.getAmmount(), price);
					System.out.println(String.format("Zakupiono %.8fBTC", sell.getAmmount()));
				}
			}
			else if(decision==(-1)) {
				
				double price = buy.getPrice()*sell.getAmmount()*(1-tax);
				
				if(portfel.sell("BTC", price)) { 
					
					portfel.add("USD", sell.getAmmount());
					System.out.println(String.format("Sprzedano %.8fBTC", buy.getAmmount()));
					
					if(portfel.profitable(price, sell.getAmmount())) System.out.println("Sprzedano z zyskiem");
					else System.out.println("Sprzedano ze strat¹");
				}
			}
			Thread.sleep(5000);
		}
    	System.out.println(portfel);
    	gielda.update(1);
    	portfel.getCurrentValue("BTC",gielda.getAsks().get(0).getPrice());
	}
	
	public static void main(String[] args) throws Exception {

		//zadania1_3(0.005);
		zadanie4(10, 0.005);
    }
}