package sorting;

import java.util.List;

public interface SortingAlgorithm<T extends Comparable<T>> {
    List<T> sort(List<T> toSort);
}
