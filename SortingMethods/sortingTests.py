import quickSort
import mergeSort
import numpy as np

def printArr(array):
    for i in range(len(array)):
        print(array[i])

def areArraysEqual(arr_first, arr_second):
    if(len(arr_first) != len(arr_second)):
        return False
    else:
        for i in range(len(arr_first)):
            if arr_first[i] != arr_second[i]:
                 return False
    
    return True


testArr = np.random.randint(low = 0, high = 100, size = 20) 
testArr_qs = testArr.copy()
testArr_ms = testArr.copy()

sortedTestArr = sorted(testArr)

quickSort.quickSortArr(testArr_qs)
mergeSort.mergeSort(testArr_ms)

if areArraysEqual(testArr_qs, sortedTestArr):
    print("Poprawne sortowanie quicksort!")
if areArraysEqual(testArr_ms, sortedTestArr):
    print("Poprawne sortowanie mergesort!")

print("QuickSort")
printArr(testArr_qs)

print("MergeSort")
printArr(testArr_ms)