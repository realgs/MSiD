package sorting;

import java.util.ArrayList;
import java.util.List;

public class MergeSort<T extends Comparable<T>> implements SortingAlgorithm<T>{

    @Override
    public List<T> sort(List<T> toSort) {
        sort(toSort, 0, toSort.size() - 1);
        return toSort;
    }

    private void sort(List<T> list, int begin, int end) {
        if (begin >= end) return;
        int half = (begin + end) / 2;
        sort(list, begin, half);
        sort(list, half + 1, end);
        merge(list, begin, half, end);
    }

    private void merge(List<T> list, int begin, int border, int end) {
        int leftPartSize = border - begin + 1;
        int rightPartSize = end - border;
        List<T> leftPart = new ArrayList<>(leftPartSize);
        List<T> rightPart = new ArrayList<>(rightPartSize);
        for (int i = 0; i < leftPartSize; i++)
            leftPart.add(list.get(begin + i));
        for (int i = 0; i < rightPartSize; i++)
            rightPart.add(list.get(border + 1 + i));
        int i = 0, j = 0;
        int k = begin;
        while (i < leftPartSize && j < rightPartSize) {
            if (leftPart.get(i).compareTo(rightPart.get(j)) < 0) {
                list.set(k, leftPart.get(i));
                i++;
            } else {
                list.set(k, rightPart.get(j));
                j++;
            }
            k++;
        }
        while (i < leftPartSize) {
            list.set(k, leftPart.get(i));
            i++;
            k++;
        }
        while (j < rightPartSize) {
            list.set(k, rightPart.get(j));
            j++;
            k++;
        }
    }
}
