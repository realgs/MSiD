import java.util.Comparator;
import java.util.LinkedList;
import java.util.List;

public class QuickSort extends Sort{




    public  <T> List<T> sort(List<T> list, Comparator<? super T> comparator) {
        List<T> result= new LinkedList<T>(quickSort(list, 0, list.size()-1,comparator));
        return result;

    }

    private static <T> int split(List<T> input, int first, int last, Comparator<? super T> comparator) {
        int i = first;
        int j = last;
        T pivot = (T) input.get((first + last) / 2);

        while(i <= j) {
            while(less(input.get(i), pivot,comparator)) {//input.get(i)< pivot
                ++i;
            }

            while(less(pivot,input.get(j),comparator)) {//input.get(j) > pivot
                --j;
            }

            if(i <= j) {
                exchange(input,input.get(i),input.get(j));

                ++i;
                --j;
            }
        }

        return i;
    }
    private static <T> List<T> quickSort(List<T> input, int left, int right,Comparator<? super T> comparator) {
        int index = split(input, left, right,comparator);
        if(left < index - 1) {
            quickSort(input, left, index - 1,comparator);
        }

        if(index < right) {
            quickSort(input, index, right,comparator);
        }
        return input;

    }
}
