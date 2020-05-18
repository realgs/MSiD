using System;

namespace SortingMethods
{
    public interface ISortingAlgorithm
    {
        string Name { get; }
        void Sort<T>(ref T[] numbers) where T : IComparable;
    }
}
