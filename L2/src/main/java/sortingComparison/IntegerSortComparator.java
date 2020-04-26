package sortingComparison;

import sorting.SortingAlgorithm;

import java.util.*;

public class IntegerSortComparator extends SortComparator<Integer> {

    public IntegerSortComparator(ArrayList<SortingAlgorithm<Integer>> sortingAlgorithms, int listSize, int measurementAmount) {
        super(sortingAlgorithms, listSize, measurementAmount);
    }

    @Override
    protected List<Integer> makeList() {
        Random random = new Random();
        List<Integer> list = new ArrayList<>(listSize);
        for (int i = 0; i < listSize; i++) {
            list.add(random.nextInt());
        }
        return list;
    }
}
