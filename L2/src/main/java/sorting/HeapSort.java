package sorting;

import java.lang.reflect.Array;
import java.util.*;

public class HeapSort<T extends Comparable<T>> implements SortingAlgorithm<T> {
    @Override
    public List<T> sort(List<T> toSort) {
        List<T> heap = builtHeap(toSort);
        for (int heapSize = heap.size() - 1; heapSize >= 0; heapSize--) {
            Collections.swap(heap, heapSize, 0);
            heapify(heap, 0, heapSize);
        }
        toSort.clear();
        toSort.addAll(heap);
        return toSort;
    }

    List<T> builtHeap(List<T> list) {
        ArrayList<T> heap = new ArrayList<>(list);
        for (int i = list.size(); i >= 0; i--) {
            heapify(heap, i, list.size());
        }
        return heap;
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
