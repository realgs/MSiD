package sorting;

import java.util.*;

public class QuickSort<T extends Comparable<T>> implements SortingAlgorithm<T> {
    private Random generator = new Random();
    @Override
    public List<T> sort(List<T> toSort) {
        if (toSort.size() < 2) {
            return toSort;
        }
        int pivotIndex = generator.nextInt(toSort.size());
        Collections.swap(toSort, 0, pivotIndex);
        T pivot = toSort.get(0);
        ArrayList<T> smaller = new ArrayList<>();
        ArrayList<T> bigger = new ArrayList<>();
        for (int i = 1; i < toSort.size(); i++) {
            T element = toSort.get(i);
            if (element.compareTo(pivot) < 0) {
                smaller.add(element);
            } else {
                bigger.add(element);
            }
        }
        List<T> toReturn = sort(smaller);
        toReturn.add(pivot);
        toReturn.addAll(sort(bigger));
        return toReturn;
    }
}
