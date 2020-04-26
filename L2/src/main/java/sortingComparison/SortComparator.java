package sortingComparison;

import sorting.SortingAlgorithm;
import java.util.*;

public abstract class SortComparator<T extends Comparable<T>> {
    private SortingAlgorithmsComparator<T> comparator;
    private int measurementAmount;
    protected int listSize;

    public SortComparator(ArrayList<SortingAlgorithm<T>> algorithms, int listSize, int measurementAmount) {
        this.listSize = listSize;
        this.measurementAmount = measurementAmount;
        comparator = new SortingAlgorithmsComparator<>(algorithms);
    }

    public void measureSort() {
        for (int i = 0; i < measurementAmount; i++) {
            List<T> list = makeList();
            comparator.measureSortingTime(list);
        }
    }

    public ArrayList<Long> getAverageSortingTimes() {
        return comparator.getAverageSortTime();
    }

    public ArrayList<Long> getTotalSortingTime() {
        return comparator.getTotalSortTime();
    }

    protected abstract List<T> makeList();
}
