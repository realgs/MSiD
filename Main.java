import java.util.Random;

public class Main 
{
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
	
	public static void main(String[] args) 
	{
		Sorting bubble = new BubbleSort(), select = new SelectSort();
		
		final int size = 40000;
		int [] los_liczby = random_array(size);
		
		System.out.println("Bubble Sort: " + bubble.sort(los_liczby));
		System.out.println("Select Sort: " + select.sort(los_liczby));
	}

}
