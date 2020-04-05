from random import randint

def bubble_sort(array):
    swapOccured = False
    for i in range(len(array)):
        for j in range(len(array)-i-1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
                swapOccured = True
        if not swapOccured:
            break
    return array

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

def merge(array, startIndex, middleIndex, endIndex):
    leftArray = array[startIndex:middleIndex+1]
    rightArray = array[middleIndex+1:endIndex+1]

    leftIndex = 0
    rightIndex = 0
    sortingIndex = startIndex

    while leftIndex < len(leftArray) and rightIndex < len(rightArray):
        if leftArray[leftIndex] < rightArray[rightIndex]:
            array[sortingIndex] = leftArray[leftIndex]
            leftIndex+=1
        else:
            array[sortingIndex] = rightArray[rightIndex]
            rightIndex+=1
        sortingIndex+=1

    while leftIndex < len(leftArray):
        array[sortingIndex] = leftArray[leftIndex]
        sortingIndex+=1
        leftIndex+=1
    
    while rightIndex < len(rightArray):
        array[sortingIndex] = rightArray[rightIndex]
        sortingIndex+=1
        rightIndex+=1

def merge_sort_rec(array, startIndex, endIndex):
    if startIndex < endIndex:
        middleIndex = (startIndex+endIndex)//2

        merge_sort_rec(array, startIndex, middleIndex)
        merge_sort_rec(array, middleIndex+1, endIndex)

        merge(array, startIndex, middleIndex, endIndex)

def merge_sort(array):
    merge_sort_rec(array, 0, len(array)-1)