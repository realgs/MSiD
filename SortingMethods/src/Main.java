import java.util.Arrays;

public class Main {

    public static void main(String[] args) {

    double arr[] = {12.32, 3.4, 3.5, 8.56, 1.24};
    int arr1[] = {2,52,12,71,3,85,23};
    int arr2[] = {2,52,12,71,3,85,23};

    QuickSort quickSort= new QuickSort();
    quickSort.sort(arr1);

    System.out.println(quickSort.toString(arr1));
    }
}
