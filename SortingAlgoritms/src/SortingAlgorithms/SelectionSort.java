package SortingAlgorithms;

import java.util.Comparator;
import java.util.List;

public class SelectionSort extends Sort{

    public <T> List<T> sort(List<T> list, Comparator<? super T> comparator) {

        for (int i = 0; i < list.size() - 1; i++) {
            int index = i;
            for (int j = i + 1; j < list.size(); j++)
                if (less(list.get(j), list.get(index), comparator)) {
                    index = j;
                }

            exchange(list, i, index);

        }

        return list;
    }

}