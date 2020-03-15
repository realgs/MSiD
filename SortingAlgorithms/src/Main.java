public class Main {

  public static void main(String[] args) {

    final double[] unsortedList1 = {1.6, -4, 2.2, 5, 2.2};
    final double[] unsortedList2 = {26.1, -3, 26, 0, -12.3};

    SortingAlgorithm heapSort = new HeapSort();
    SortingAlgorithm quickSort = new QuickSort();

    heapSort.sort(unsortedList1, 5);
    System.out.println(heapSort.toString());
    quickSort.sort(unsortedList2, 5);
    System.out.println(quickSort.toString());

  }

}
