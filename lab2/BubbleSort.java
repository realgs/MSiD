public class BubbleSort implements Sorting
{
	@Override
	public long sort(int[] tab) 
	{
		int [] liczby = tab.clone();
		long start = System.currentTimeMillis(); 		
		boolean swaped;
		int temp;
		
		for(int i=0; i<liczby.length-1; i++)
		{
			swaped = false;
			for(int j=0; j<liczby.length-1; j++)
			{
				if(liczby[j]>liczby[j+1])
				{
					swaped = true;
					temp = liczby[j];
					liczby[j] = liczby[j+1];
					liczby[j+1] = temp;
				}
			}
			if (swaped==false) break;
		}
		return ( System.currentTimeMillis() - start);
	}
	
}