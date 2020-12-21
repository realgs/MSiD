
public class MergeSort<T extends Comparable<T>> implements SortingAlgorithm<T> {


    public void sort(T arr[]){
        mergesort(arr,0,arr.length-1);
    }

    void merge(T arr[], int l, int m, int r)
    {
        int n1 = m - l + 1;
        int n2 = r - m;


        T L[] = (T[]) new Comparable[n1];
        T R[] = (T[]) new Comparable[n1];


        for (int i=0; i<n1; ++i)
            L[i] = arr[l + i];
        for (int j=0; j<n2; ++j)
            R[j] = arr[m + 1+ j];


        int i = 0, j = 0;

        int k = l;
        while (i < n1 && j < n2)
        {//L[i] <= R[j]
            if (L[i].compareTo(R[j])<0)

            {
                arr[k] = L[i];
                i++;
            }
            else
            {
                arr[k] = R[j];
                j++;
            }
            k++;
        }

        while (i < n1)
        {
            arr[k] = L[i];
            i++;
            k++;
        }

        while (j < n2)
        {
            arr[k] = R[j];
            j++;
            k++;
        }
    }


    void mergesort(T arr[], int l, int r)
    {
        if (l < r)
        {
            int m = (l+r)/2;

            mergesort(arr, l, m);
            mergesort(arr , m+1, r);

            merge(arr, l, m, r);
        }
    }

}

