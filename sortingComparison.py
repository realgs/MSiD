from datetime import datetime

def sortBubble(array):
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(array) - 1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True
    return array

array = [5, 2, 1, 8, 4]
print("Test for Bubble Sort: ")
print(sortBubble(array))

def sortQucik_partition(array):
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

def sortQucik(array):
    if len(array) <= 1:
        return array

    low, pivot, high = sortQucik_partition(array)

    return sortQucik(low) + [pivot] + sortQucik(high)

array = [5,3,4,2,7,6,1]
print("Test for Quick Sort: ")
print (sortQucik(array))

def sortMerge_merge(left, right):
    """
    Traverse both sorted sub-arrays (left and right), and populate the result array
    """
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]

    return result

def sortMerge(array):
    """
    Sequence of numbers is taken as input, and is split into two halves, following which they are recursively sorted.
    """
    if len(array) < 2:
        return array

    mid = len(array) // 2     # note: 7//2 = 3, whereas 7/2 = 3.5

    left_sequence = sortMerge(array[:mid])
    right_sequence = sortMerge(array[mid:])

    return sortMerge_merge(left_sequence, right_sequence)

array = [5,2,6,8,5,8,1,2,4,6,6]
print("Test for Merge Sort: ")
print (sortMerge(array))

def sortHeap_heapify(nums, heap_size, root_index):
    largest = root_index
    left_child = (2 * root_index) + 1
    right_child = (2 * root_index) + 2

    if left_child < heap_size and nums[left_child] > nums[largest]:
        largest = left_child

    if right_child < heap_size and nums[right_child] > nums[largest]:
        largest = right_child

    if largest != root_index:
        nums[root_index], nums[largest] = nums[largest], nums[root_index]
        sortHeap_heapify(nums, heap_size, largest)   # note: Heapify the new root element to ensure it's the largest

def sortHeap(array):
    length = len(array)
    """
    The 2nd argument of range means we stop iteration at the id before -1 (first element)
    The 3rd argument of range means we iterate backwards
    """
    for i in range(length, -1, -1):
        sortHeap_heapify(array, length, i)

    for i in range(length - 1, 0, -1):  # note: Move the root of the max heap to the end of
        array[i], array[0] = array[0], array[i]
        sortHeap_heapify(array, i, 0)

    return array

array = [4, 5, 2, 3, 5, 6, 7, 1]
print("Test for Heap Sort: ")
print(sortHeap(array))
print("\n")


def measureTimeForSortingAlgorithms(bubbleMethodToRun, quickMethodToRun, mergeMethodToRun, heapMethodToRun, array):
    print("Present time for sorting algorithms:")

    startTime = datetime.now()
    bubbleMethodToRun(array)
    print("Time taken via bubbleMethod:",(datetime.now() - startTime))

    startTime = datetime.now()
    quickMethodToRun(array)
    print("Time taken via quickMethod:",(datetime.now() - startTime))

    startTime = datetime.now()
    mergeMethodToRun(array)
    print("Time taken via mergeMethod:",(datetime.now() - startTime))

    startTime = datetime.now()
    heapMethodToRun(array)
    print("Time taken via heapMethod:",(datetime.now() - startTime))

array = [ 1, 99, 4, 3, 43, 5, 3, 8, 5, 5, 1, 4, 345, 3, 5, 34343, 6, 3, 5, 2, 7, 1, 2, 1, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 8, 5, 1, 6566, 4, 3, 5, 1, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 55, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 78, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 8, 5, 1, 4, 22, 3, 5, 1, 2, 4, 3, 8, 5, 1, 4, 3, 44, 5, 1, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 44, 8, 5, 1, 4, 3, 34534534534534, 5, 1, 2, 4, 3, 834, 5, 1, 13, 4, 3, 5, 90, 1, 2, 4, 23, 3, 8, 5, 1, 4, 3, 13, 5, 1, 2, 4, 3, 8, 5, 1, 4, 3, 15, 11, 2, 4, 3, 4, 3, 5, 33, 34, 1, 2, 3, 11, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 4534, 2, 4, 3, 8, 33, 1, 4, 3, 5, 122, 2, 4, 3, 8, 43, 44, 2, 33, 1, 556, 43, 3, 5, 143, 2, 4, 3, 8, 5, 1, 4, 454645, 3, 8, 5, 1, 4, 4, 3, 5, 143, 2, 4, 3, 8, 5, 1, 4, 4, 3, 8, 5, 1, 4,3, 5, 1, 234, 3, 4, 5, 666, 2, 4, 3, 4, 3, 8, 5, 1, 4, 3, 54444, 1, 2, 4, 3, 8, 5, 1, 4, 3, 5, 1, 2, 454645, 1, 2, 1, 2343434, 1, 1, 232, 3, 1, 1, 1323, 1, 1, 1, 12, 4, 3, 4, 3, 8, 5, 1, 4, 3, 54444, 1, 2, 4, 3, 2, 4, 3, 4, 3, 8, 5, 1, 4, 3, 54444, 1, 2, 4, 3, 1, 2, 1, 2, 1, 2, 2, 54444, 1, 2, 4, 3, 2, 4, 3, 4, 3, 8, 5, 1, 4, 3, 54444, 1, 2, 4, 3, 1, 2, 1, 2, 1, 2, 2, 54444, 1, 2, 4, 3, 2, 4, 3, 4, 3, 8, 5, 1, 4, 3, 54444, 1, 2, 4, 3, 1, 2, 1, 2, 1, 2, 2, 1, 34, 34, 6346, 23, 4]
measureTimeForSortingAlgorithms(sortMerge, sortQucik, sortMerge, sortHeap, array)