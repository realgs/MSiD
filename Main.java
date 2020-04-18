import java.util.Random;

public class Main 
{
	private static int [] losuj_tab(int n)
	{
		Random r = new Random();
		int [] tab = new int[n];
		
		for(int i=0; i<n; i++)
		{
			liczby[i]=r.nextInt(10000);
		}
		
		return tab;
	}
	
	@SuppressWarnings("unused")
	public static void main(String[] args) 
	{
		Sorting bubble = new Bubble(),  merge = new Merge(), insert = new Insert(), quick = new Quick();
		
		int [] losowa = losuj_tab(10000);
		
		System.out.println("TABLICA LOSOWA: ");
		System.out.println("Bubble Sort: " + bubble.sort(losowa));
		System.out.println("Merge Sort: " + merge.sort(losowa));
		System.out.println("Insert Sort: " + insert.sort(losowa));
		System.out.println("Quick Sort: " + quick.sort(losowa));
		
	}

}