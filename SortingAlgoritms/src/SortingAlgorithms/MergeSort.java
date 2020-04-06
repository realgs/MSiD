package SortingAlgorithms;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedList;
import java.util.List;

public class MergeSort extends Sort {



    public  <T> List<T> sort(List<T> list, Comparator<? super T> comparator) {


        if (list.size() > 1) {
            split(list,comparator);

        }
        LinkedList<T> result = new LinkedList<T>(list);


        return result;

    }


    private static <T> List<T> split(List<T> inputArray, Comparator<? super T> comparator) {
        if (inputArray.size() > 1) {
            List<T> left = new ArrayList<T>();
            List<T> right = new ArrayList<T>();
            for (int i = 0; i < inputArray.size(); i++) {
                if (i < inputArray.size() / 2) {
                    left.add(inputArray.get(i));
                } else {
                    right.add(inputArray.get(i));
                }
            }
            split(left, comparator);
            split(right, comparator);
            merge(inputArray, left, right, comparator);
        }

        return inputArray;

    }

    private static <T> void merge(List<T> result, List<T> left, List<T> right, Comparator<? super T> comparator) {
        int i1 = 0;
        int i2 = 0;

        for (int i = 0; i < result.size(); i++) {
            if (i2 >= right.size() || (i1 < left.size() &&
                    less(left.get(i1), right.get(i2), comparator))) {
                result.set(i, left.get(i1));
                i1++;
            } else {
                result.set(i, right.get(i2));
                i2++;
            }
        }
    }

}
