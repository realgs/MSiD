import java.util.ArrayList;

public class InsertSort<T extends Comparable<? super T>> implements ListSorter<T> {
    @Override
    public void sort(ArrayList<T> list) {
        for (int i = 1; i < list.size(); ++i) {
            T value = list.get(i);
            int j;
            for (j = i; j > 0 && value.compareTo(list.get(j-1))<0; j--)
                list.set(j,list.get(j-1));
            list.set(j, value);
        }
    }

    @Override
    public String toString() {
        return "InsertSort";
    }
}
