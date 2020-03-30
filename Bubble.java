public class Bubble implements Sorting {
	@Override
	public long sort(int[] tab) {
		int [] tablica = tab.clone(); 
		long start = System.currentTimeMillis(); 
		
		
		for(int i=0; i<tablica.length-1; i++)
		{
			for(int j=0; j<tablica.length-i-1; j++)
			{
				if(tablica[j]>tablica[j+1])
				{
					int swap = tablica[j];
					tablica[j] = tablica[j+1];
					tablica[j+1] = swap;
				}
			}
		}
		
		return ( System.currentTimeMillis() - start);
	}
	
}
