package sorting;

import java.security.cert.CollectionCertStoreParameters;
import java.util.*;

public class SortingMethods {
    private static Random generator = new Random();

    public static <T extends Comparable<T>> List<T> quicksort(List<T> toSort) {
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
        List<T> toReturn = quicksort(smaller);
        toReturn.add(pivot);
        toReturn.addAll(quicksort(bigger));
        return toReturn;
    }

    public static <T extends Comparable<T>> List<T> selectionSort(List<T> toSort) {
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