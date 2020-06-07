import java.util.ArrayList;

public class HeapSort <T extends Comparable<? super T>> implements ArrayListSorter<T> {

    @Override
    public void sort(ArrayList<T> list) {
        heapAdjustment(list, list.size());
        for (int i = list.size() - 1; i > 0; i--) {
            swap(list, i, 0);
            heapify(list, 0, i);
        }
    }

    private void swap(ArrayList<T> list, int left, int right) {
        T temp = list.get(left);
        list.set(left, list.get(right));
        list.set(right, temp);
    }

    public void heapify(ArrayList<T> heap, int index, int n) {
        int indexOfBigger = 2 * index + 1;
        if (indexOfBigger < n) {
            if (indexOfBigger + 1 < n && heap.get(indexOfBigger).compareTo(heap.get(indexOfBigger + 1)) < 0) {
                indexOfBigger++;
            }
            
            if (heap.get(index).compareTo(heap.get(indexOfBigger)) < 0) {
                swap(heap, index, indexOfBigger);
                heapify(heap, indexOfBigger, n);
            }
        }
    }

    void heapAdjustment(ArrayList<T> heap, int n) {
        for (int i = (n - 1) / 2; i >= 0; i--) {
            heapify(heap, i, n);
        }
    }
}
