import java.util.ArrayList;
import java.util.Random;

public class QuickSort<T extends Comparable<? super T>> implements ListSorter<T> {
    Random random = new Random();

    @Override
    public void sort(ArrayList<T> list) {
        quicksort(list, 0, list.size());
    }

    private void quicksort(ArrayList<T> list, int startIndex, int endIndex) {
        if (endIndex - startIndex > 1) {
            int partition = partition(list, startIndex, endIndex);
            quicksort(list, startIndex, partition);
            quicksort(list, partition + 1, endIndex);
        }
    }

    private int partition(ArrayList<T> list, int nFrom, int nTo) {
        int rnd = nFrom + random.nextInt(nTo - nFrom);
        swap(list, nFrom, rnd);
        T value = list.get(nFrom);
        int idxBigger = nFrom + 1, idxLower = nTo - 1;
        do {
            while (idxBigger <= idxLower && list.get(idxBigger).compareTo(value) <= 0)
                idxBigger++;
            while (list.get(idxLower).compareTo(value) > 0)
                idxLower--;
            if (idxBigger < idxLower)
                swap(list, idxBigger, idxLower);
        } while (idxBigger < idxLower);
        swap(list, idxLower, nFrom);
        return idxLower;
    }

    private void swap(ArrayList<T> list, int left, int right) {
        if (left != right) {
            T temp = list.get(left);
            list.set(left, list.get(right));
            list.set(right, temp);
        }
    }

    @Override
    public String toString() {
        return "QuickSort";
    }
}
