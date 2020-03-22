from random import randint

def insert_sort(array):
    for i in range(len(array)):
        value = array[i]
        j = i
        while(j>0 and array[j-1] > value):
            array[j] = array[j-1]
            j-=1
        array[j] = value

def quick_sort(array):
    quick_sort_rec(array, 0, len(array)-1)

def partition(array, startIndex, endIndex):
    pivotIndex = randint(startIndex, endIndex)
    pivot = array[pivotIndex]
    smallerIndex = startIndex-1
    for currentIndex in range(startIndex, endIndex):
        if array[currentIndex] < pivot:
            smallerIndex+=1
            array[smallerIndex], array[currentIndex] = array[currentIndex], array[smallerIndex]
    array[smallerIndex+1], array[pivotIndex] = array[pivotIndex], array[smallerIndex+1]
    return (smallerIndex+1)

def quick_sort_rec(array, startIndex, endIndex):
    if startIndex < endIndex: 
        partitionIndex = partition(array, startIndex, endIndex)
        quick_sort_rec(array, startIndex, partitionIndex-1)
        quick_sort_rec(array, partitionIndex+1, endIndex)


numbers = [234, 4, -2, 15, 9, -30, 999]
quick_sort(numbers)
print(numbers)
