import java.util.List;

public class SelectionSort<T extends Comparable<? super T>> implements Sort<T>{


    void sort(List<T> list) {
        if(list.size() == 0) return;
        T min = list.get(0);
        int min_index = 0;
        for(int i = 1; i < list.size(); i++){
            if(list.get(i).compareTo(min) < 0){
                min = list.get(i);
                min_index = i;
            }
        }

        list.set(min_index, list.get(0));
        list.set(0, min);
        List<T> newList = list.subList(1, list.size());
        this.sort(newList);
    }

}