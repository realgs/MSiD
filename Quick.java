public class QuickSort implements Sorting {
	
	@Override
	public long sort(int[] tab) 
	{
		int [] liczby = tab.clone();
		long start = System.currentTimeMillis(); 
		
		qsort(liczby,0,liczby.length-1);
		
		return ( System.currentTimeMillis() - start);
	}

	private void qsort(int[] tab, int begin, int end)
	{
		int i = begin, j = end, pivot, temp;
		
		pivot = tab[ (begin+end)/2 ];
		
		while (i<=j)
		{
			while (tab[i]<pivot) i++;
			
			while (pivot<tab[j]) j--;
			
			if (i<=j) 
			{
				temp=tab[i];
				tab[i]=tab[j];
				tab[j]=temp;
				i++;
				j--;
			}
		}
		
		if (begin<j) qsort(tab,begin,j);
		if (i<end) qsort(tab,i,end);
	}
	
}
