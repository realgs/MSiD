import java.util.ArrayList;

public class MergeSort<T extends Comparable<? super T>> implements ArrayListSorting<T> {

    @Override
    public void sort(ArrayList<T> list) {
        sort(list, 0, list.size() - 1);
    }

    private void sort(ArrayList<T> list, int l, int r) {
        if (l < r) {
            int m = (l + r) / 2;
            sort(list, l, m);
            sort(list, m + 1, r);
            merge(list, l, m, r);
        }
    }

    private void merge(ArrayList<T> list, int l, int m, int r) {
        int size1 = m - l + 1;
        int size2 = r - m;

        ArrayList<T> L = new ArrayList<>(list.subList(l, l + size1));
        ArrayList<T> R = new ArrayList<>(list.subList(m + 1, m + 1 + size2));

        int i = 0, j =0;

        int k = l;
        while (i < size1 && j < size2) {
            if (L.get(i).compareTo(R.get(j)) <= 0) {
                list.set(k, L.get(i));
                ++i;
            } else {
                list.set(k, R.get(j));
                ++j;
            }
            ++k;
        }

        while (i < size1) {
            list.set(k, L.get(i));
            ++i;
            ++k;
        }

        while (j < size2) {
            list.set(k, R.get(j));
            ++j;
            ++k;
        }
    }
}
