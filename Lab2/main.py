from sortingmethods import quick_sort, insert_sort, bubble_sort
from random import randint

def main():
    minValue = -100
    maxValue = 100
    arraySize = 10
    array1 = [randint(minValue, maxValue) for _ in range(0, arraySize)]
    array2 = array1.copy()
    array3 = array1.copy()

    print("Before insertion sort: \n%s" % array1)
    insert_sort(array1)
    print("After inserion sort: \n%s" % array1)

    print("Before quick sort: \n%s" % array2)
    quick_sort(array2)
    print("After quick sort: \n%s" % array2)

    print("Before bubble sort: \n%s" % array3)
    bubble_sort(array3)
    print("After bubble sort: \n%s" % array3)

if __name__ == "__main__":
    main()