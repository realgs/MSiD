import java.util.*;

public class BogoSort <T extends Comparable<? super T>>
{
    public static void main(String[] args)
    {
        BogoSort<Integer> bongos = new BogoSort<>();
        Integer[] testArray = {12,5,124,214,1,2,0,5,11,13,15};
        System.out.println(java.util.Arrays.toString(testArray));
        bongos.sort(testArray);
    }

    void sort(T[] array)
    {
        List<T> list = Arrays.asList(array);
        long i=0;
        while(!isSorted(list)) {
            Collections.shuffle(list);
            i++;
            if(i%1000000 == 0)
                System.out.println("Just a second");
        }

        System.out.println("Finally!");
        System.out.println(Arrays.toString(list.toArray()));
    }


    public  <T extends Comparable<? super T>>
    boolean isSorted(Iterable<T> iterable) {
        Iterator<T> iter = iterable.iterator();
        if (!iter.hasNext()) {
            return true;
        }
        T t = iter.next();
        while (iter.hasNext()) {
            T t2 = iter.next();
            if (t.compareTo(t2) > 0) {
                return false;
            }
            t = t2;
        }
        return true;
    }
}
