import java.util.Random;

public class Main 
{
	final int size = 40000;
	int [] los_liczby = random_array(size);
	
	private static int [] random_array(int n)
	{
		int [] liczby = new int[n];
		Random r = new Random();
		for(int i=0; i<n; i++)
		{
			liczby[i]=r.nextInt(10000);
		}
		
		return liczby;
	}
	
	public static long comparesort(Sorting sorting_method)
	{
		return sorting_method.sort(los_liczby);
	}	
	
	public static void main(String[] args) 
	{
		Sorting bubble = new BubbleSort(), select = new SelectSort(),
				heap = new HeapSort(), quick = new QuickSort();
		
		System.out.println("Bubble Sort: " + comparesort(bubble));
		System.out.println("Select Sort: " + comparesort(select));
		System.out.println("Heap Sort: " + comparesort(heap));
		System.out.println("Quick Sort: " + comparesort(quick));
		System.out.println("____________________________________");
	}

}