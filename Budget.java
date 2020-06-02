import java.util.ArrayList;

public class Budget 
{
	public class Resource 
	{
		String currency;
		double ammount;
		
		public Resource(String currency, double ammount)
		{
			this.currency = currency;
			this.ammount = ammount;
		}

		@Override
		public String toString() 
		{
			if(currency.equals("USD")) return currency + " Iloœæ: "+ String.format("%.2f", ammount);
			else return currency + " Iloœæ: "+ String.format("%.8f", ammount);
		}
	}

	ArrayList<Resource> resources;
	ArrayList<Offer> bought;
	
	public Budget()
	{
		resources = new ArrayList<Resource>();
		bought = new ArrayList<Offer>();
	}
	
	public void add(String currency, double ammount)
	{
		boolean added = false;
		for(Resource res : resources) 
		{
			if(res.currency.equals(currency))
			{
				res.ammount+=ammount;
				added = true; 
				break;
			}
			
		}
		if(!added) resources.add(new Resource(currency, ammount));
	}
	
	public void add(String currency, double ammount, double boughtPrice)
	{
		add(currency, ammount);
		bought.add(new Offer(false,boughtPrice,ammount));
	}
	
	public boolean sell(String currency, double ammount)
	{
		for(Resource res: resources)
		{
			if(res.currency.equals(currency) && res.ammount >= ammount)
			{
				res.ammount-=ammount;
				System.out.println("\nSprzedano walute: "+currency+"\tw ilosci: "+ammount);
				return true;
			}
		}
		
		System.out.println("Brak wystarczajacej iloœci waluty "+currency);
		return false;
	}

	public boolean profitAvailable(double price, double ammount)
	{
		double sum = 0;
		
		for(Offer o : bought)
		{
			if(o.price<=price) sum+=o.ammount;
		}
		
		return sum>=ammount;
	}
	
	@Override
	public String toString() 
	{
		String output="[BUD¯ET]\n";
		for(Resource res : resources)
		{
			output+=res+"\n";
		}
		
		return output;
	}
	
	
}

