import java.util.ArrayList;

public class InsertSort <T extends Comparable<? super T>> implements ArrayListSorting<T>{

    @Override
    public void sort (ArrayList<T> list) {
        int size = list.size();
        for (int i = 1; i < size; ++i) {
            T key = list.get(i);
            int j;
            for (j = i - 1; j > -1 && list.get(j).compareTo(key) > 0; --j)
                list.set(j + 1, list.get(j));

            list.set(j + 1, key);
        }
    }

    @Override
    public String toString() {
        return "InsertSort";
    }
}