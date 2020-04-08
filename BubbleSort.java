import java.util.ArrayList;

public class BubbleSort<T extends Comparable<? super T>> implements ArrayListSorter<T> {
    @Override
    public void sort(ArrayList<T> list) {
        for(int pass = 1 ; pass < list.size() ; ++pass){
            for(int leftElementIndex = 0 ; leftElementIndex < (list.size() - pass) ; ++leftElementIndex){
                if(list.get(leftElementIndex).compareTo(list.get(leftElementIndex + 1)) > 0){
                    swap(list, leftElementIndex, leftElementIndex + 1);
                }
            }
        }
    }

    private void swap(ArrayList<T> list, int leftIndex, int rightIndex){
        T element = list.get(leftIndex);
        list.set(leftIndex, list.get(rightIndex));
        list.set(rightIndex, element);
    }
}
