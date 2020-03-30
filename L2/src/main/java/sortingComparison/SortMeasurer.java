package sortingComparison;

import sorting.SortingAlgorithm;
import java.util.List;

public class SortMeasurer<T extends Comparable<T>> {
    private final SortingAlgorithm<T> algorithm;

    public SortMeasurer(SortingAlgorithm<T> algorithm) {
        this.algorithm = algorithm;
    }

    public long getSortingTime(List<T> toSort) {
        long startTime = System.currentTimeMillis();
        algorithm.sort(toSort);
        long finishTime = System.currentTimeMillis();
        return finishTime - startTime;
    }
}
