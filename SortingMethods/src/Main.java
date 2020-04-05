import java.util.Arrays;

public class Main {

    public static void main(String[] args) {

    Double arr[] = {12.32, 3.5, 3.4, 8.56, 1.24};
    Integer arr1[] = {2,52,12,71,3,85,23};
    String arr3[]={"ala","kuba","ania","adam","patryk"};
    Integer arr2[] = {2,52,12,71,3,85,23};
    Double arr4[] = {12.32, 3.4, 3.5, 8.56, 1.24};

    SortingAlgorithm<Integer> quickSort= new QuickSort();
    quickSort.sort(arr1);
    SortingAlgorithm<Double> quickSortd= new QuickSort();
    quickSortd.sort(arr);
    SortingAlgorithm<String> quickSorts= new QuickSort();
    quickSorts.sort(arr3);
    SortingAlgorithm<Integer> mergeSort= new MergeSort();
    mergeSort.sort(arr2);
    SortingAlgorithm<Double> bitonicSort = new BitonicSort();
    bitonicSort.sort(arr4);
    System.out.println(Arrays.toString(arr));
    System.out.println(Arrays.toString(arr1));
    System.out.println(Arrays.toString(arr3));
    System.out.println(Arrays.toString(arr2));
    System.out.println(Arrays.toString(arr4));

    }
}
