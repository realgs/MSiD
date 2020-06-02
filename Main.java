import java.io.IOException;

public class Main 
{
	final static String [] api_names = {"BitBay","Cex.IO","WhiteBit","FTX"};
	
	final static String [] pairs = {"BTC", "USD", 
			  						"ETH", "USD",
			  						"LTC", "USD",
			  						"ETH", "BTC"};
	
    public static void update(Orderbook [][] data, int xsize, int ysize) throws IOException
    {
    	for(int i=0; i<xsize; i++)
    	{
    		for(int j=0; j<ysize; j++)
        	{
        		data[i][j].update(1);
        	}
    	}
    }
    
    public static void arbitrage(Budget budget, Orderbook [][] data, int exchange, int market, int size, double tax)
    {
    	
    	Offer buy = data[exchange][market].sell.get(0);
    	Offer sell, best=null;
    	Double profit=0.0, bestProfit=0.0;
    	
    	for(int i=0; i<size ; i++)
    	{
    		if(i==exchange) continue;
    		
    		sell = data[i][market].buy.get(0);
    		profit=(sell.price-buy.price*(1+tax))*Math.min(buy.ammount, sell.ammount);
    		
    		if(pairs[2*market+1].equals("USD"))
    		{
    			profit*=100;
    			profit=Math.floor(profit);
    			profit/=100;
    		}
    		
    		if(profit>0)
    		{
    			System.out.println("Na gie³dzie "+ api_names[exchange] +" mo¿na kupiæ "+ Math.min(buy.ammount, sell.ammount) + 
    								" " +pairs[2*market] +" po kursie "+ buy.price + pairs[2*market+1]+ 
    									" i sprzedaæ na gie³dzie "+ api_names[i]  +" po kursie "+ sell.price + " " + pairs[2*market+1] +
    										" zyskuj¹c " + String.format("%.8f", profit)+ " "+pairs[2*market+1]);
    			
    			if(profit>bestProfit)
    			{
    				best=sell;
    				bestProfit=profit;
    			}
    		}
    	}
    	
    	if(best!=null)
    	{
    		budget.add(pairs[2*market+1], bestProfit);
    	}
    }
	
    public static void zad1_3() throws Exception
    {
    	Budget budget = new Budget();
    	Orderbook[][] dane = new Orderbook[4][4];
    	
    	for(int i=0; i<4; i++)
    	{
    		dane[0][i] = new BitBayOrderbook(pairs[2*i], pairs[2*i+1]);
    	}
    	for(int i=0; i<4; i++)
    	{
    		dane[1][i] = new CexIoOrderbook(pairs[2*i], pairs[2*i+1]);
    	}
    	for(int i=0; i<4; i++)
    	{
    		dane[2][i] = new WhiteBitOrderbook(pairs[2*i], pairs[2*i+1]);
    	}
    	for(int i=0; i<4; i++)
    	{
    		dane[3][i] = new FtxOrderbook(pairs[2*i], pairs[2*i+1]);
    	}
    	
    	for(int rep=0; rep<1; rep++)
    	{
    		System.out.println("Pobieranie danych.");
    		update(dane, 4, 4);
    		System.out.println("Pobrano dane.");
        	for(int i=0; i<4; i++)
        	{
        		for(int j=0; j<4; j++)
        		{
        			arbitrage(budget, dane, i, j, 4, 0.0005); // np. 0.001 oznacza prowizjê na poziomie 0,1%
        		}
        		System.out.println();
        	}
        	if(!budget.resources.isEmpty()) System.out.println(budget);
    	}
    }
    
    public static void zad4() throws Exception
    {
    	Budget budget = new Budget();
		Orderbook cex = new CexIoOrderbook("BTC","USD");
		Agent agent = new Agent("BTCdata.csv", cex);
		
		budget.add("USD", 17000);
		budget.sell("USD", 3000);
		budget.sell("USD", 4000);
		budget.sell("USD", 11000);
		budget.add("BTC", 0.007362);
		budget.sell("BTC", 0.007);
		budget.sell("BTC", 0.007);
		System.out.println(budget);
		
//		for(int i=0; i<10; i++)
//		{
//			System.out.println();
//			cex.update(1);
//	    	agent.makeDecision(cex, 50, 100, 0);
//	    	Thread.sleep(10000);
//		}
    }
    
	public static void main(String[] args) throws Exception 
    {	
		//zad1_3();
		zad4();
    }
}