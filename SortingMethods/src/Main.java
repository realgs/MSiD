import java.util.Arrays;

public class Main {

    public static void main(String[] args) {

    double arr[] = {12.32, 3.4, 3.5, 8.56, 1.24};
    int arr1[] = {2,52,12,71,3,85,23};
    int arr2[] = {2,52,12,71,3,85,23};

    SortingAlgorithm quickSort= new QuickSort();
    quickSort.sort(arr1);
    SortingAlgorithm mergeSort= new MergeSort();
    mergeSort.sort(arr2);

    System.out.println(Arrays.toString(arr1));
    System.out.println(Arrays.toString(arr2));
    }
}
