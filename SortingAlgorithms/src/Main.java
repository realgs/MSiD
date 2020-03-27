public class Main {

  public static void main(String[] args) {

    final double[] unsortedList = {1.6, -4, 2.2, 5, 2.2};

    SortingAlgorithm heapSort = new HeapSort();
    SortingAlgorithm quickSort = new QuickSort();

    heapSort.sort(unsortedList, 5);
    System.out.println(heapSort.toString());
    quickSort.sort(unsortedList, 5);
    System.out.println(quickSort.toString());

  }

}
