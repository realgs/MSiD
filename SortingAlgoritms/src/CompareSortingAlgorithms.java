import SortingAlgorithms.InsertionSort;
import SortingAlgorithms.MergeSort;
import SortingAlgorithms.QuickSort;
import SortingAlgorithms.SelectionSort;

import java.util.*;

public class CompareSortingAlgorithms {

    private MergeSort mergeSort;
    private QuickSort quickSort;
    private InsertionSort insertionSort;
    private SelectionSort selectionSort;

    public CompareSortingAlgorithms() {
        quickSort = new QuickSort();
        mergeSort = new MergeSort();
        insertionSort = new InsertionSort();
        selectionSort = new SelectionSort();

    }

    public  <T> String compare(List<T> list, Comparator<? super T> comparator) {
        Map< Long,String> results = new TreeMap<>();


        results.put(mergeSort.get_execution_time(list, comparator,System.nanoTime()),"MergeSort");
        results.put(quickSort.get_execution_time(list, comparator,System.nanoTime()), "QuickSort");
        results.put(insertionSort.get_execution_time(list, comparator, System.nanoTime()),"InsertionSort");
        results.put(selectionSort.get_execution_time(list, comparator, System.nanoTime()),"SelectionSort");


        String result = "Algoritms performance from best to worst: \n";
        int index = 1;
        for (Long res : results.keySet()) {
            result +=index+". "+results.get(res) + " : " + res + " [ns] \n";
            index++;
        }
        return result;
    }


}
