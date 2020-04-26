def partition(array):
    pivot = array[0]
    i = 1
    for j in range(i, len(array)):
        if array[j] < pivot:
            temp = array[i]
            array[i] = array[j]
            array[j] = temp
            i += 1
    array[0] = array[i-1]
    array[i-1] = pivot
    return array[0:i-1], pivot, array[i:(len(array))]


def quick_sort(array):
    if len(array) <= 1:
        return array

    low, pivot, high = partition(array)

    return quick_sort (low) + [pivot] + quick_sort (high)

array = [5,3,4,2,7,6,1]

print (quick_sort(array))