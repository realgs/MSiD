package sorting;

import java.util.*;

public class HeapSort<T extends Comparable<T>> implements SortingAlgorithm<T> {
    @Override
    public List<T> sort(List<T> toSort) {
        toSort = builtHeap(toSort);
        for (int toSortSize = toSort.size() - 1; toSortSize >= 0; toSortSize--) {
            Collections.swap(toSort, toSortSize, 0);
            heapify(toSort, 0, toSortSize);
        }
        return toSort;
    }

    List<T> builtHeap(List<T> list) {
        for (int i = list.size(); i >= 0; i--) {
            heapify(list, i, list.size());
        }
        return list;
    }

    private void heapify(List<T> list, int currentElement, int size) {
        if (currentElement >= size) return;
        int leftChild = getLeftChild(currentElement);
        int rightChild = getRightChild(currentElement);
        heapifySubtree(list, currentElement, leftChild, size);
        heapifySubtree(list, currentElement, rightChild, size);
    }

    private void heapifySubtree(List<T> list, int currentElement, int child, int size) {
        if (child >= size) return;
        if (list.get(child).compareTo(list.get(currentElement)) > 0) {
            Collections.swap(list, currentElement, child);
        }
        heapify(list, child, size);
    }

    int getLeftChild(int parent) {
        return  parent * 2 + 1;
    }

    int getRightChild(int parent) {
        return  parent * 2 + 2;
    }
}
