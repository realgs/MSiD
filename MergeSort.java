import java.util.ArrayList;
import java.util.Iterator;

public class MergeSort<T extends Comparable<? super T>> implements Sort<T>{

    @Override
    public void sort(ArrayList<T> list) {
        mergesort(list, 0, list.size() - 1);
    }

    @SuppressWarnings("unchecked")
    private ArrayList<T> mergesort(ArrayList<T> list, int startIndex, int endIndex) {
        if (startIndex == endIndex) {
            ArrayList<T> result = new ArrayList<T>();
            result.add(list.get(startIndex));
            return result;
        }
        int splitIndex = startIndex + (endIndex - startIndex) / 2;
        return merge(mergesort(list, startIndex, splitIndex),
                mergesort(list, splitIndex + 1, endIndex));
    }

    @SuppressWarnings("unchecked")
    private ArrayList<T> merge(ArrayList<T> left, ArrayList<T> right) {
        ArrayList<T> result = new ArrayList<T>();
        Iterator<T> l = left.iterator();
        Iterator<T> r = right.iterator();
        T elemL = null, elemR = null;
        boolean contL, contR;
        if (contL = l.hasNext()) elemL = l.next();
        if (contR = r.hasNext()) elemR = r.next();
        while (contL && contR) {
            if ((elemL).compareTo(elemR) <= 0) {
                result.add(elemL);
                if (contL = l.hasNext()) elemL = l.next();
                else result.add(elemR);
            }
            else {
                result.add(elemR);
                if (contR = r.hasNext()) elemR = r.next();
                else result.add(elemL);
            }
        }
        while (l.hasNext()) result.add(l.next());
        while (r.hasNext()) result.add(r.next());
        return result;
    }
}
