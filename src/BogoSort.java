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

    public void sort(ArrayList<T> array)
    {

        long i=0;
        long start = System.currentTimeMillis();
        long time = System.currentTimeMillis();
        //System.out.println("Finally!");
        while(!isSorted(array) && (time-start)<10000){
            Collections.shuffle(array);
            i++;
            time = System.currentTimeMillis();
        }
        if(isSorted(array))
        System.out.println("Finally!");
        else
            System.out.println("Sorry i couldn't make it :C");
        //System.out.println(array.toString());
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
