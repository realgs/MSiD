import java.util.ArrayList;

public class BubbleSort<T extends Comparable<? super T>> {

    public void sort(ArrayList<T> list){
        boolean isSorting = true;
        while(isSorting) {
            isSorting = false;
            for (int i = 0; i < list.size() - 1; i++) {
                if (list.get(i).compareTo(list.get(i + 1)) > 0) {
                    T swapHelper = list.get(i);
                    list.set(i, list.get(i + 1));
                    list.set(i + 1, swapHelper);
                    isSorting = true;
                }
            }
        }
    }
}