import java.util.ArrayList;
import java.util.Random;

public class StalinSort <T extends Comparable<? super T>> extends Sorting<T>{
    public static void main(String[] args) {
        StalinSort<Integer> stalin = new StalinSort<>();
        Random r = new Random();
        ArrayList<Integer> testArray1 = new ArrayList<>();
        ArrayList<String> testArray2 = new ArrayList<>();
        for (int i = 0; i < 50; i++) {
            testArray1.add(r.nextInt(201) - 100);
            testArray2.add(Integer.toString(r.nextInt(201) - 100));
        }
        stalin.sort(testArray1);

    }
       public void sort (ArrayList<T> array) {
            int length = array.size();
            for (int i = 1; i < length; i++) {
                if (array.get(i).compareTo(array.get(i - 1)) < 0) {
                    array.remove(i);
                    length--;
                    i--;
                }

            }
           // System.out.println(array.toString());
        }




}

