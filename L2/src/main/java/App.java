import sorting.*;
import sortingComparison.IntegerSortComparator;

import java.util.*;

public class App {
    public static void main(String[] args) {
        final int algorithmAmount = 4;
        final int measurementAmount = 100;
        final int testListSize = 10000;
        ArrayList<SortingAlgorithm<Integer>> algorithms = new ArrayList<>(algorithmAmount);
        String[] algorithmsNames = {"quick sort", "merge sort", "heap sort", "selection sort"};
        algorithms.add(new QuickSort<>());
        algorithms.add(new MergeSort<>());
        algorithms.add(new HeapSort<>());
        algorithms.add(new SelectionSort<>());
        IntegerSortComparator sortComparator = new IntegerSortComparator(algorithms, testListSize, measurementAmount);
        sortComparator.measureSort();
        ArrayList<Long> averageTime =  sortComparator.getAverageSortingTimes();
        ArrayList<Long> totalTime =  sortComparator.getTotalSortingTime();
        for (int i = 0; i < algorithms.size(); i++) {
            System.out.println(algorithmsNames[i] + ": average " + averageTime.get(i) + " total:" + totalTime.get(i));
        }
    }
}
/*
quick sort: average 3 total:384
merge sort: average 2 total:255
heap sort: average 408 total:40898
selection sort: average 219 total:21936
 */