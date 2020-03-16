public class HeapSort<T extends Comparable<? super T>>  //not quite sure why, have to read more about Comparable
{
    public static void main(String[] args)
    {
        Integer[] testArray = {12,5,124,214,1,2,564,6,3,2,1,78,4,2,543,33,0};
        HeapSort<Integer> Sorter = new HeapSort<>();
        Sorter.heapSort(testArray);
        System.out.println(java.util.Arrays.toString(testArray));
    }

    void heapSort(T[] array)
    {
        int size = array.length;
        for (int i = size / 2 - 1; i > -1; i--)
            heapify(array, size, i);

        for (int i = size - 1; i > -1; i--)
        {
            T temp = array[0];
            array[0] = array[i];
            array[i] = temp;

            heapify(array, i, 0);
        }
    }

    void heapify(T[] array, int size, int i)
    {
        int max = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < size && array[left].compareTo(array[max]) > 0)
            max = left;

        if (right < size && array[right].compareTo(array[max]) > 0)
            max = right;

        if (max != i)
        {
            T temp = array[i];
            array[i] = array[max];
            array[max] = temp;

            heapify(array, size, max);
        }
    }
}