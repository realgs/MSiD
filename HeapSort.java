public class HeapSort implements Sorting
{

	@Override
	public long sort(int[] tab) 
	{
		int [] liczby = tab.clone(); 
		long start = System.currentTimeMillis(); 
		
		heapsort(liczby,0,liczby.length-1);
		
		return ( System.currentTimeMillis() - start);
	}

	private void heapsort(int[] tab, int begin, int end)
	{
		int n = tab.length;
		
		for(int i = (n/2-1); i>=0; i--)
		{
			heapify(tab, n, i);
		}
		
		for(int i = n-1; i>=0; i--)
		{
			int swap = tab[0];
			tab[0] = tab[i];
			tab[i] = swap; 
		
			heapify(tab, i, 0);
		}
	}

	private void heapify(int [] tab, int n, int i) 
	{
		int largest = i;
		int left = 2*i+1;
		int right = 2*i+2;
		
		if(left < n && tab[left] > tab[largest]) largest = left;
		
		if(right < n && tab[right] > tab[largest]) largest = right;
		
		if(largest != i)
		{
			int swap = tab[i];
			tab[i] = tab[largest];
			tab[largest] = swap;
			
			heapify(tab, n, largest);
		}
		
	}
	
}