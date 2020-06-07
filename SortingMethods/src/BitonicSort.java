public class BitonicSort<T extends Comparable<T>> implements SortingAlgorithm<T> {

    public void sort(T a[])
    {
        bitonicSort(a, 0, a.length, true); //true ascending false descending
    }

    void compAndSwap(T a[], int i, int j, boolean dir)
    {
            if (dir==(a[i].compareTo(a[j])>0))
        {
            T temp = a[i];
            a[i] = a[j];
            a[j] = temp;
        }
    }

    void bitonicMerge(T a[], int low, int cnt, boolean dir)
    {
        if (cnt>1)
        {
            int k=greatestPowerOfTwoLessThan(cnt);
            for (int i=low; i<low+cnt-k; i++)
                compAndSwap(a,i, i+k, dir);
            bitonicMerge(a,low, k, dir);
            bitonicMerge(a,low+k, cnt-k, dir);
        }
    }

    void bitonicSort(T a[], int low, int cnt, boolean dir)
    {
        if (cnt>1)
        {
            int k = cnt/2;

            bitonicSort(a, low, k, !dir);
            bitonicSort(a,low+k, cnt-k, dir);
            bitonicMerge(a, low, cnt, dir);
        }
    }
    int greatestPowerOfTwoLessThan(int cnt)
    {
        int k=1;
        while (k>0 && k<cnt)
            k=k<<1;
        return k>>>1;
    }

}