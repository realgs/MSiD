from sortingmethods import quick_sort, insert_sort
from random import randint

def main():
    array1 = [randint(-100, 100) for _ in range(0, 10)]
    array2 = array1.copy()
    print("Before insertion sort: %s" % array1)
    insert_sort(array1)
    print("After inserion sort: %s" % array1)

    print("Before quick sort: %s" % array2)
    quick_sort(array2)
    print("After quick sort: %s" % array2)

if __name__ == "__main__":
    main()