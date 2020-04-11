import java.util.ArrayList;
import static java.util.Collections.swap;

public class BubbleSort<T extends Comparable<? super T>> implements Sort {

    @Override
    public void sort(ArrayList list) {
        bubbleSort(list);
    }

    ArrayList<T> bubbleSort(ArrayList<T> list){
        int rightMaxIndex = list.size() - 1;
        while(rightMaxIndex > 0){
            int lastChecked = 0;
            for(int i=0; i<rightMaxIndex; i++){
                if((list.get(i)).compareTo(list.get(i+1)) < 0) {
                    swap(list, i, i + 1);
                    lastChecked = i;

                }
            }
            rightMaxIndex = lastChecked;
        }
        return list;
    }
}