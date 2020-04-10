import java.util.ArrayList;

public class BubbleSort<T extends Comparable<? super T>> implements ArrayListSorting<T>{

    @Override
    public void sort (ArrayList<T> list) {
        int size = list.size();
        T tmp;
        for (int i = 1; i < size; ++i)
            for (int j = 1; j <= size - i; ++j)
                if (list.get(j - 1).compareTo(list.get(j)) > 0) {
                    //arr[j - 1] > arr[j]
                    tmp = list.get(j - 1);
                    list.set(j - 1, list.get(j));
                    list.set(j, tmp);
                }
    }

}