import java.util.ArrayList;

public class QuickSort<T extends Comparable<? super T>> implements ArrayListSorting<T> {

    @Override
    public void sort(ArrayList<T> list) {
        sort(list, 0, list.size() - 1);
    }

    private void sort(ArrayList<T> list, int low, int high) {
        if (low < high) {
            int p = partition(list, low, high);
            sort(list, low, p - 1);
            sort(list, p + 1, high);
        }
    }

    private int partition(ArrayList<T> list, int low, int high) {
        T pivot = list.get(high);
        int i = low - 1;
        for (int j = low; j < high; ++j) {
            if (list.get(j).compareTo(pivot) < 0) {
                ++i;
                T tmp = list.get(i);
                list.set(i, list.get(j));
                list.set(j, tmp);
            }
        }
        T tmp = list.get(i + 1);
        list.set(i + 1, list.get(high));
        list.set(high, tmp);

        return i + 1;
    }
}
