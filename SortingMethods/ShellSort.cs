using System;
using System.Collections.Generic;
using System.Linq;

namespace SortingMethods
{
    public class ShellSort : ISortingAlgorithm
    {
        public string Name => $"Shell sort ({_shellSortSeries.Description()})";
        private readonly ShellSortSeries _shellSortSeries;

        public ShellSort(ShellSortSeries s)
        {
            _shellSortSeries = s;
        }

        public void Sort<T>(ref T[] numbers) where T : IComparable
        {
            int len = numbers.Length;
            IEnumerable<int> gapSeries = GenerateGapSeries(len);
            foreach (int gap in gapSeries)
            {
                for (int i = gap; i < len; ++i)
                {
                    T tmp = numbers[i];
                    int j;
                    for (j = i; j >= gap && numbers[j - gap].CompareTo(tmp) == 1; j -= gap)
                    {
                        numbers[j] = numbers[j - gap];
                    }

                    numbers[j] = tmp;
                }
            }
        }

        private IEnumerable<int> GenerateGapSeries(int len)
        {
            var gapSeries = new List<int>();
            int k, i;
            switch (_shellSortSeries)
            {
                case ShellSortSeries.Shell:
                    k = 1;
                    do
                    {
                        i = (int) (len / Math.Pow(2, k));
                        ++k;
                        gapSeries.Add(i);
                    } while (i > 1);
                    break;
                case ShellSortSeries.FrankLazarus:
                    k = 1;
                    do
                    {
                        i = (int) (2 * len / Math.Pow(2, k + 1));
                        ++k;
                        gapSeries.Add(i);
                    } while (i > 1);
                    break;
                default:
                    throw new ArgumentOutOfRangeException();
            }

            if(gapSeries.Last() != 1) gapSeries.Add(1);
            return gapSeries;
        }
    }
}