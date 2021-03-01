import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

public class ArrayDefaultSort<T extends Comparable<? super T>> {


    public void sort(ArrayList<T> array){
        Collections.sort(array);
       // System.out.println(array.toString());

    }
}
