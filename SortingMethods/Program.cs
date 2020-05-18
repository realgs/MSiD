using System;

namespace SortingMethods
{
    class Program
    {
        static void Main(string[] args)
        {
            float[] numbersToSort1 = { 1.6f, 6.5f, 1.5f, 1.55f, 1.51f, -6, 3, 5, 21 };
            int[] numbersToSort2 = { 1021, 6, 5, 5, 0, 0, 3};

            ISortingAlgorithm quicksort = new Quicksort();
            ISortingAlgorithm mergesort = new MergeSort();

            Console.WriteLine($"Numbers before sorting:");
            Console.WriteLine(string.Join(' ', numbersToSort1));
            Console.WriteLine(string.Join(' ', numbersToSort2));

            quicksort.Sort(ref numbersToSort1);
            mergesort.Sort(ref numbersToSort2);

            Console.WriteLine($"Numbers after sorting:");
            Console.WriteLine(string.Join(' ', numbersToSort1));
            Console.WriteLine(string.Join(' ', numbersToSort2));
        }
    }
}
