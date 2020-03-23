public class SelectSort implements Sorting
{
	@Override
	public void sort(int[] tab) 
	{
		int [] liczby = tab.clone(); 
		long start = System.currentTimeMillis(); 
		int swap, min_index;
		
		for(int i=0; i<liczby.length-1; i++)
		{
			min_index = i;
			
			for(int j=i+1; j<liczby.length; j++)
			{
				if(liczby[j] < liczby[min_index])
				{
					min_index = j;
				}
			}
			swap = liczby[i];
			liczby[i]=liczby[min_index];
			liczby[min_index] = swap;
		}
		
	}

}