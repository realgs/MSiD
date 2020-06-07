import java.util.ArrayList;
import java.util.List;

public class InsertionSort<T extends Comparable<? super T>> implements Sort<T>{

    void sort(List<T> list){
        for(int i = 1; i < list.size(); i++){
            int i_index = i;

            while( i_index > 0 && list.get(i_index - 1).compareTo(list.get(i_index)) > 0){
                T swapHelp = list.get(i_index);
                list.set(i_index, list.get(i_index - 1));
                list.set(i_index - 1, swapHelp);
                i_index--;
            }

        }
    }

}
