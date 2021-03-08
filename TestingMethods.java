import java.util.ArrayList;
import java.util.Random;

public class TestingMethods {
    private int noOfItems;
    private boolean partiallyOrdered;

    TestingMethods() {
        this.noOfItems = 1000000;
        this.partiallyOrdered = false;
    }

    TestingMethods(int listSize, boolean partiallyOrdered) {
        this.noOfItems = listSize;
        this.partiallyOrdered = partiallyOrdered;
    }

    private ArrayList<Integer> creatIntegerArray() {
        Random rand = new Random();
        ArrayList<Integer> newArrayList = new ArrayList<>();
        if (partiallyOrdered) {
            for (int i = 0; i < noOfItems; i++) {
                int numberToAdd = i;
                if (i % 15 == 0) {
                    numberToAdd = rand.nextInt(noOfItems * 2);
                }
                Integer element = numberToAdd;
                newArrayList.add(element);
            }
        } else {
            for (int i = 0; i < noOfItems; i++) {
                Integer numberToAdd = rand.nextInt(2001);
                newArrayList.add(numberToAdd);
            }
        }
        return newArrayList;
    }
    
    private long getRunningTime(Sort<Integer> sortingMethod) {
        long startTime, endTime, durationTime;
        startTime = System.currentTimeMillis();
        ArrayList<Integer> array = creatIntegerArray();
        sortingMethod.sort(array);
        endTime = System.currentTimeMillis();
        return durationTime = endTime - startTime;
    }

    void compareSort() {
        Sort<Integer> bubble = new BubbleSort<>();
        Sort<Integer> merge = new MergeSort<>();
        Sort<Integer> quick = new QuickSort<>();
        Sort<Integer> heap = new HeapSort<>();

        ArrayList<Sort<Integer>> array = new ArrayList<>();
        array.add(bubble);
        array.add(merge);
        array.add(quick);
        array.add(heap);

        long bubbleSortTime = getRunningTime(array.get(0));
        System.out.println("Czas trwania sortowania BubbleSort: " + bubbleSortTime );
        long mergeSortTime = getRunningTime(array.get(1));
        System.out.println("Czas trwania sortowania MergeSort: " + mergeSortTime );
        long quickSortTime = getRunningTime(array.get(2));
        System.out.println("Czas trwania sortowania QuickSort: " + quickSortTime );
        long heapSortTime = getRunningTime(array.get(3));
        System.out.println("Czas trwania sortowania HeapSort: " + heapSortTime );
    }
}