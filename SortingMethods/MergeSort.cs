using System;

namespace SortingMethods
{
    public class MergeSort : ISortingAlgorithm
    {
        public string Name => "Merge sort";

        public void Sort<T>(ref T[] numbers) where T : IComparable
        {
            if(numbers.Length < 2) return;
            Sort(ref numbers, 0, numbers.Length);
        }

        private void Sort<T>(ref T[] numbers, int low, int high) where T : IComparable
        {
            int n = high - low;
            if(n<=1) return;
            int mid = low + n / 2;
            Sort(ref numbers, low, mid);
            Sort(ref numbers, mid, high);

            var a = new T[n];
            int i = low, j = mid;
            for (int k = 0; k < n; ++k)
            {
                if (i == mid) a[k] = numbers[j++];
                else if (j == high) a[k] = numbers[i++];
                else if (numbers[j].CompareTo(numbers[i]) == -1) a[k] = numbers[j++];
                else a[k] = numbers[i++];
            }

            for (int k = 0; k < n; k++)
                numbers[low + k] = a[k];
        }

    }
}
