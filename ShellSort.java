import java.util.ArrayList;
import java.util.Arrays;

public class ShellSort<T extends Comparable<? super T>> implements ListSorter<T> {
    @Override
    public void sort(ArrayList<T> list) {
        Integer[] distanceTable = new Integer[]{0, 1, 4, 10, 23, 57, 132, 301, 701};
        sort(list, distanceTable);
    }

    private void sort(ArrayList<T> list, Integer[] distanceTable){
        int size = list.size();
        int iterator = 1;
        int distance = distanceTable[distanceTable.length - iterator];
        while(distance > 0){
            for(int i = distance; i < size; i++){
                T value = list.get(i);
                int otherIndex;
                for(otherIndex = i; otherIndex >= distance && (value).compareTo(list.get(otherIndex - distance)) < 0; otherIndex -= distance)
                    list.set(otherIndex, list.get(otherIndex - distance));
                list.set(otherIndex,value);
            }
            distance = distanceTable[distanceTable.length - ++iterator];
        }
    }

    @Override
    public String toString() {
        return "ShellSort";
    }
}
