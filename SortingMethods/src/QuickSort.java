public class QuickSort<T extends Comparable<T>> implements SortingAlgorithm<T>{

    public void sort(T arr[]){
        quicksort(arr,0,arr.length-1);
    }

    void swap (T arr[],int i, int j){
        T temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    int partition(T arr[], int low, int high)
    {
        T pivot = arr[high];
        int i = (low-1);
        for (int j=low; j<high; j++)
        {
            if (arr[j].compareTo(pivot)<0)
            {
                i++;
                swap(arr,i,j);
            }
        }

        swap(arr,i+1,high);

        return i+1;
    }

    void quicksort(T arr[], int low, int high)
    {
        if (low < high)
        {
            int pi = partition(arr, low, high);

            quicksort(arr, low, pi-1);
            quicksort(arr, pi+1, high);
        }
    }


}
