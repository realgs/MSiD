import java.util.*;

public class BogoSort <T extends Comparable<? super T>>
{
    public static void main(String[] args)
    {
        BogoSort<Integer> bongos = new BogoSort<>();
        Random r = new Random();
        ArrayList<Integer> testArray1 = new ArrayList<>();
        ArrayList<String> testArray2 = new ArrayList<>();
        for(int i=0;i<10; i++){
            testArray1.add(r.nextInt(201)-100);
            testArray2.add(Integer.toString(r.nextInt(201)-100));
        }
        bongos.sort(testArray1);
    }

    void sort(ArrayList<T> array)
    {

        long i=0;
        while(!isSorted(array)) {
            Collections.shuffle(array);
            i++;
            if(i%1000000 == 0)
                System.out.println("Just a second");
        }

        System.out.println("Finally!");
        System.out.println(array.toString());
    }


    public  <T extends Comparable<? super T>> boolean isSorted(Iterable<T> iterable) {
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
