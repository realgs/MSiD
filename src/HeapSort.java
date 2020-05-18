import java.util.ArrayList;
import java.util.Random;


public class HeapSort<T extends Comparable<? super T>> extends Sorting<T> //not quite sure why, have to read more about Comparable
{
    public static void main(String[] args)
    {
        Integer[] testArray = {12,5,124,214,1,2,564,6,3,2,1,78,4,2,543,33,0};

        HeapSort<Integer> Sorter = new HeapSort<>();
        HeapSort<String> Sorter2 = new HeapSort<>();
        Random r = new Random();
        ArrayList<Integer> testArray1 = new ArrayList<>();
        ArrayList<String> testArray2 = new ArrayList<>();
        for(int i=0;i<50; i++){
            testArray1.add(r.nextInt(201)-100);
            testArray2.add(Integer.toString(r.nextInt(201)-100));
    }


        Sorter.sort(testArray1);
        Sorter2.sort(testArray2);
    }

    public void sort(ArrayList<T> array)
    {
        int size = array.size();
        for (int i = size / 2 - 1; i > -1; i--)
            heapify(array, size, i);

        for (int i = size - 1; i > -1; i--)
        {
            T temp = array.get(0);
            array.set(0, array.get(i));
            array.set(i, temp);

            heapify(array, i, 0);
        }
        //System.out.println(array.toString());
    }

    void heapify(ArrayList<T> array, int size, int i)
    {
        int max = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < size && array.get(left).compareTo(array.get(max)) > 0)
            max = left;

        if (right < size && array.get(right).compareTo(array.get(max)) > 0)
            max = right;

        if (max != i)
        {
            T temp = array.get(i);
            array.set(i, array.get(max));
            array.set(max, temp);
            heapify(array, size, max);
        }
    }
}