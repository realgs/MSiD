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
