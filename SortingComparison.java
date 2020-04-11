import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class SortingComparison {

    public static long measureSorting(Sort sort, List list){
        long startTime = System.currentTimeMillis();
        sort.sort(list);
        long endTime = System.currentTimeMillis();
        return   endTime - startTime;
    }

    public static void main(String[] Args){

        ArrayList<Integer> testListOne = new ArrayList<>();
        ArrayList<Integer> testListTwo = new ArrayList<>();
        ArrayList<Integer> testListThree = new ArrayList<>();
        ArrayList<Integer> testListFour = new ArrayList<>();
        Random random = new Random();
        for(int i = 0; i < 1000; i++){
            int randomElement = random.nextInt(10000);
            testListOne.add(randomElement);
            testListTwo.add(randomElement);
            testListThree.add(randomElement);
            testListFour.add(randomElement);
        }
        BubbleSort<Integer> bs = new BubbleSort<>();
        InsertionSort<Integer> is = new InsertionSort<>();
        SelectionSort<Integer> ss = new SelectionSort<>();
        QuickSort<Integer> qs = new QuickSort<>();

        long bubbleSortTime = measureSorting(bs, testListOne);
        long insertionSortTime = measureSorting(is, testListTwo);
        long selectionSortTime = measureSorting(ss, testListThree);
        long quickSortTime = measureSorting(qs, testListFour);

        System.out.println("BubbleSort time : " + bubbleSortTime + "ms");
        System.out.println("InsertionSort time : " + insertionSortTime + "ms");
        System.out.println("SelectionSort time : " + selectionSortTime + "ms");
        System.out.println("QuickSort time : " + quickSortTime + "ms");

    }

}
