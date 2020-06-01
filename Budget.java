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
		public String toString() {
			return currency + " Iloœæ: "+ String.format("%.8f", ammount);
		}
	}

	ArrayList<Resource> resources;
	
	public Budget()
	{
		resources = new ArrayList<Resource>();
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

