import java.util.ArrayList;

public class Wallet {
	
	private class Fund {
		
		String currency;
		double ammount;
		
		private Fund(String currency, double ammount) {
			this.currency = currency;
			this.ammount = ammount;
		}

		@Override
		public String toString() {
			if(currency.equals("USD")) return String.format("%.2f", ammount)+currency;
			else return String.format("%.8f", ammount)+currency;
		}
	}

	ArrayList<Fund> funds;
	ArrayList<Offer> bought;
	
	public Wallet() {
		funds = new ArrayList<Fund>();
		bought = new ArrayList<Offer>();
	}
	
	public Wallet(String currency, double startingFunds) {
		
		funds = new ArrayList<Fund>();
		bought = new ArrayList<Offer>();
		add(currency, startingFunds);
	}
	
	public void add(String currency, double ammount) {
		
		boolean added = false;
		for(Fund f : funds) {
			
			if(f.currency.equals(currency)) {
				
				f.ammount+=ammount;
				added = true; 
				break;
			}
			
		}
		if(!added) funds.add(new Fund(currency, ammount));
	}
	
	public void add(String currency, double ammount, double boughtPrice) {
		
		add(currency, ammount);
		bought.add(new Offer(boughtPrice,ammount));
	}
	
	public boolean sell(String currency, double ammount) {
		
		for(Fund f: funds) {
			
			if(f.currency.equals(currency) && f.ammount >= ammount) {
				
				f.ammount-=ammount;
				System.out.println("\nSprzedano "+ammount+currency);
				return true;
			}
		}
		
		System.out.println("Brak œrodków na wykonanie transakcji!");
		return false;
	}

	public boolean profitable(double price, double ammount) {
		
		double sum = 0;
		
		for(Offer o : bought) {
			
			if(o.getPrice()<=price) sum+=o.getAmmount();
		}
		
		return sum>=ammount;
	}
	
	public double getCurrentValue(String currency, double price) {
		
		double value=0.0;
		
		for(Fund f : funds) {
			
			if(f.currency=="USD") value+=f.ammount;
			else if(f.currency=="BTC") value+=(f.ammount*price);
		}
		
		return value;
	}
	
	@Override
	public String toString() {
		
		String output="WALLET\n";
		for(Fund f : funds) {
			
			output+=f+"\n";
		}
		
		return output;
	}
}