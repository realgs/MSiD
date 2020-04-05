from sortingmethods import quick_sort, insert_sort, bubble_sort, merge_sort
from sortingcomparator import compareAll
from random import randint

def main():
    minValue = -100
    maxValue = 100
    arraySize = 5000
    array = [randint(minValue, maxValue) for _ in range(0, arraySize)]
    functions = [bubble_sort, insert_sort, quick_sort, merge_sort]
    compareAll(functions, array)

if __name__ == "__main__":
    main()