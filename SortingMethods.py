
def swap(some_list, index1, index2):
    some_list[index1], some_list[index2] = some_list[index2], some_list[index1]


def bubble_sort(sortable_list):
    n = len(sortable_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if sortable_list[j] > sortable_list[j + 1]:
                swap(sortable_list, j, j + 1)


def partition(array, start_index, end_index):
    pivot = array[end_index]
    i = start_index
    for j in range(start_index, end_index):
        if array[j] < pivot:
            swap(array, i, j)
            i = i + 1
    swap(array, i, end_index)
    return i


def quick_sort_ranged(array, start_index, end_index):
    if start_index < end_index:
        p = partition(array, start_index, end_index)
        quick_sort_ranged(array, start_index, p - 1)
        quick_sort_ranged(array, p + 1, end_index)


def quick_sort(array):
    quick_sort_ranged(array, 0, len(array) - 1)


def insert_sort(array):
    i = 1
    while i < len(array):
        x = array[i]
        j = i - 1
        while j >= 0 and array[j] > x:
            array[j + 1] = array[j]
            j = j - 1
        array[j + 1] = x
        i += 1


# Marcin Ciura's gap sequence
gaps = [701, 301, 132, 57, 23, 10, 4, 1]


def shell_sort(array):
    for gap in gaps:
        for i in range(gap, len(array)):
            tmp = array[i]
            j = i
            while j >= gap and array[j - gap] > tmp:
                array[j] = array[j - gap]
                j = j - gap
            array[j] = tmp
