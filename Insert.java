public class InsertSort implements Sorting {

	@Override
	public long sort(int[] tab) 
	{
		int [] liczby = tab.clone(); 
		long start = System.currentTimeMillis(); 
		
		for(int i=1; i<liczby.length; i++)
		{
			int wartosc = liczby[i];
			int j = i-1;
			
			while(j>=0 && liczby[j] > wartosc)
			{
				liczby[j+1] = liczby[j];
				j--;
			}
			liczby[j+1] = wartosc;
		}
		
		return ( System.currentTimeMillis() - start);
	}

}
