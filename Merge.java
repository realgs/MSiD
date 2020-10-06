public class Merge implements Sorting {

	@Override
	public long sort(int[] tab) {
		int [] liczby = tab.clone(); 
		long start = System.currentTimeMillis(); 
		mergesort(liczby, 0, liczby.length-1);
		return ( System.currentTimeMillis() - start);
	}

	private void mergesort(int [] tab, int begin, int end) {
		if(begin < end)
		{
			int half = (begin+end)/2;
			
			mergesort(tab, begin, half);
			mergesort(tab, half+1, end);
			
			merge(tab, begin, half, end);
		}
		
	}
	
	private void merge(int [] tab, int begin, int half, int end) {
		
		int lsize = half-begin+1, rsize=end-half;
		int [] L = new int [lsize]; 
		int [] R = new int [rsize]; 
		
		for(int i=0; i<lsize; i++) { L[i] = tab[begin+i]; }
		for(int i=0; i<rsize; i++) { R[i] = tab[half+i+1]; }
		
		int l=0, r=0, k=begin;
		
		while( l<lsize && r<rsize )
		{
			if(L[l]<R[r])
			{
				tab[k] = L[l];
				l++;
			}
			else
			{
				tab[k] = R[r];
				r++;
			}
			k++;
		}
		
		while (l < lsize) 
		{ 
	        tab[k] = L[l]; 
	        l++; 
	        k++; 
	    } 
	  
	    while (r < rsize) 
		{ 
	        tab[k] = R[r]; 
	        r++; 
	        k++; 
	    } 
		
	}
}
