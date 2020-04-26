package sorting;

import java.util.Collections;
import java.util.List;

public class SelectionSort<T extends Comparable<T>> implements SortingAlgorithm<T> {
    @Override
    public List<T> sort(List<T> toSort) {
        for (int i = 0; i < toSort.size(); i++) {
            int min = i;
            for (int j = i; j < toSort.size(); j++) {
                if (toSort.get(j).compareTo(toSort.get(min)) < 0) {
                    min = j;
                }
            }
            Collections.swap(toSort, i, min);
        }
        return toSort;
    }
}
