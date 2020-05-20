using System;
using System.Collections.Generic;

namespace SortingMethods
{
    class Program
    {
        private static readonly List<ISortingAlgorithm> SortingAlgorithms = new List<ISortingAlgorithm> {
            new Quicksort(),
            new ShellSort(ShellSortSeries.Shell),
            new ShellSort(ShellSortSeries.FrankLazarus),
            new MergeSort(),
        };

        private static readonly List<List<float>> ToSort = new List<List<float>>
        {
            new List<float>{ 1.6f, 6.5f, 1.5f, 1.55f, 1.51f, -6, 3, 5, 21 },
            new List<float>{ 1021, 6, 5, 5, 0, 0, 3 },
        };

        private static void Main()
        {
            StartFullSimulation();
        }

        private static void StartFullSimulation()
        {
            foreach (ISortingAlgorithm algorithm in SortingAlgorithms)
            {
                foreach (List<float> numbersToSortReadonly in ToSort)
                {
                    float[] numbersToSort = numbersToSortReadonly.ToArray();
                    Console.WriteLine($"Simulating {algorithm.Name}");
                    Console.WriteLine($"Numbers before sorting: {string.Join(' ', numbersToSort)}");
                    double timeInSeconds = TimeMeasurer.Measure(() => algorithm.Sort(ref numbersToSort)).TotalSeconds;
                    Console.WriteLine($"Numbers after sorting: {string.Join(' ', numbersToSort)}");
                    Console.WriteLine($"Time taken: {timeInSeconds}");
                }
            }

            Console.WriteLine("Press any key to continue...");
            Console.ReadKey();
        }
    }
}
