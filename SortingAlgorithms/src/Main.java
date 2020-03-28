import java.util.Random;

public class Main {

  public static double[] generateArray(int size){
    double[] retArr = new double[size];
    Random rand = new Random();

    for(int i = 0; i < size; i++){
      retArr[i] = (double) Math.round(size * 100 * rand.nextDouble()) / 100;
    }

    return retArr;

  }

  public static void main(String[] args) {

    final double[] unsortedList = {1.6, -4, 2.2, 5, 2.2};
    final double[] generatedList = generateArray(10);

    SortingAlgorithm heapSort = new HeapSort();
    SortingAlgorithm quickSort = new QuickSort();
    SortingAlgorithm insertionSort = new InsertionSort();
    SortingAlgorithm pancakeSort = new PancakeSort();

    heapSort.sort(generatedList, 5);
    System.out.println(heapSort.toString());
    quickSort.sort(generatedList, 5);
    System.out.println(quickSort.toString());
    insertionSort.sort(generatedList, 5);
    System.out.println(insertionSort.toString());
    pancakeSort.sort(generatedList, 5);
    System.out.println(pancakeSort.toString());

  }

}
