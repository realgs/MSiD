using System;

namespace SortingMethods
{
    public class Quicksort : ISortingAlgorithm
    {
        public string Name => "Quicksort";

        public void Sort<T>(ref T[] numbers) where T : IComparable
        {
            Sort(ref numbers, 0, numbers.Length - 1);
        }

        private static void Sort<T>(ref T[] numbers, int low, int high) where T : IComparable
        {
            if (low >= high) return;
            int p = Partition(ref numbers, low, high);
            Sort(ref numbers, low, p);
            Sort(ref numbers, p + 1, high);
        }

        private static int Partition<T>(ref T[] numbers, int low, int high) where T : IComparable
        {
            T pivot = numbers[(low + high) / 2];
            int i = low - 1;
            int j = high + 1;
            while (true)
            {
                do
                {
                    ++i;
                } while (numbers[i].CompareTo(pivot) == -1);
                do
                {
                    --j;
                } while (numbers[j].CompareTo(pivot) == 1);

                if (i >= j) return j;

                Swap(ref numbers, i, j);
            }

        }

        private static void Swap<T>(ref T[] numbers, int i, int j)
        {
            T tmp = numbers[i];
            numbers[i] = numbers[j];
            numbers[j] = tmp;
        }
    }
}
