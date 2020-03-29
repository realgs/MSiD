import java.util.ArrayList;
import java.util.Random;

public class TimeTest {
    public static void main(String[] args){
        HeapSort<Integer> sorter1 = new HeapSort<>();
        BogoSort<Integer> sorter2 = new BogoSort<>();
        StalinSort<Integer> sorter3 = new StalinSort<>();
        ArrayDefaultSort<Integer> sorter4 = new ArrayDefaultSort<>();

        testSortingMethods(sorter1,100,10);
       // testSortingMethods(sorter2,100,10);
        testSortingMethods(sorter3,100,10);
        testSortingMethods(sorter4,100,10);
    }
    public static void testSortingMethods(Sorting<Integer> test, int arraySize,int attemps){
        ArrayList<Integer> array = new ArrayList<Integer>();
        Random r = new Random();
        long time = 0, begin = 0;
        for(int j = 0; j<attemps; j++){
            array.clear();
            for(int i=0;i<arraySize; i++){
                array.add(r.nextInt(1001));
            }
            begin = System.nanoTime();
            test.sort(array);
            time += System.nanoTime() - begin;
        }
        System.out.println("Averange time for " + test.getClass().getName() + " = " + time/1000000 + "ms");
    }


}
