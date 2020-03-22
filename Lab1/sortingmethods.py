from random import randint

def insert_sort(array):
    for i in range(len(array)):
        value = array[i]
        j = i
        while(j>0 and array[j-1] > value):
            array[j] = array[j-1]
            j-=1
        array[j] = value

def partition(array, startIndex, endIndex):
    pivotIndex = randint(startIndex, endIndex)
    array[startIndex], array[pivotIndex] = array[pivotIndex], array[startIndex]
    pivot = array[startIndex]
    smallerIndex = startIndex
    for currentIndex in range(startIndex+1, endIndex+1):
        if array[currentIndex] < pivot:
            smallerIndex+=1
            array[currentIndex], array[smallerIndex] = array[smallerIndex], array[currentIndex]
    array[smallerIndex], array[startIndex] = array[startIndex], array[smallerIndex]
    return smallerIndex

def quick_sort_rec(array, startIndex, endIndex):
    if startIndex < endIndex: 
        partitionIndex = partition(array, startIndex, endIndex)
        quick_sort_rec(array, startIndex, partitionIndex-1)
        quick_sort_rec(array, partitionIndex+1, endIndex)

def quick_sort(array):
    quick_sort_rec(array, 0, len(array)-1)

numbers = [4, 8, 9, 3, -59, 123, -345, 10, -10, 10]
quick_sort(numbers)
print(numbers)