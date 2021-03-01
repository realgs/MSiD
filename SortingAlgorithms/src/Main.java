import java.util.ArrayList;
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

    final int sizeOfArray = 100000;

    //final double[] unsortedList = {1.6, -4, 2.2, 5, 2.2};
    final double[] generatedList = generateArray(sizeOfArray);
    SortComparator compare = new SortComparator();

    ArrayList<SortingAlgorithm> sortingAlgorithms = new ArrayList<>();

    sortingAlgorithms.add(new HeapSort());
    sortingAlgorithms.add(new QuickSort());
    sortingAlgorithms.add(new InsertionSort());
    sortingAlgorithms.add(new PancakeSort());

    compare.compareAlgorithms(sortingAlgorithms, generatedList, sizeOfArray);
    compare.printResults();

  }
}
