public class SelectSort implements Sorting
{
	@Override
	public void sort(int[] tab) 
	{
		int [] liczby = tab.clone(); 
		int temp, min_index;
		
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
			temp = liczby[i];
			liczby[i]=liczby[min_index];
			liczby[min_index] = temp;
		}
		
	}

}
