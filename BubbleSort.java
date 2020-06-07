public class BubbleSort implements Sorting
{
	@Override
	public void sort(int[] tab) 
	{
		int [] liczby = tab.clone(); 
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
	}
	
}
