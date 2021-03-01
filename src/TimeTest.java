import java.util.ArrayList;
import java.util.Random;

public class TimeTest {
    public static void main(String[] args){
        ArrayList<Integer> testArray1 = new ArrayList<>();
        ArrayList<Integer> testArray2 = new ArrayList<>();
        ArrayList<Integer> testArray3 = new ArrayList<>();
        ArrayList<Integer> testArray4 = new ArrayList<>();

        HeapSort<Integer> Sorter1 = new HeapSort<>();
        BogoSort<Integer> Sorter2 = new BogoSort<>();
        StalinSort<Integer> Sorter3 = new StalinSort<>();
        ArrayDefaultSort<Integer> Sorter4 = new ArrayDefaultSort<>();

        int length = 20;
        int v = 0;
        long start,time1,time2,time3,time4;
        Random r = new Random();

        for(int i=0;i<length; i++){
            v= r.nextInt(201)-100;
            testArray1.add(v);
            testArray2.add(v);
            testArray3.add(v);
            testArray4.add(v);
           }

                start=System.nanoTime();
        Sorter1.sort(testArray1);
        time1=System.nanoTime();
        Sorter2.sort(testArray2);
        time2=System.nanoTime();
        Sorter3.sort(testArray3);
        time3=System.nanoTime();
        Sorter4.sort(testArray4);
        time4=System.nanoTime();

        System.out.println("HeapSort time: "+(time1-start) + "\t" + testArray1.toString());
        System.out.println("BogoSort time: "+(time2-time1) + "\t"  +testArray2.toString());
        System.out.println("StalinSort time: " +(time3-time2) + "\t" +testArray3.toString());
        System.out.println("DefaultSort time: " +(time4-time3) + "\t" +testArray4.toString());

    }
}
