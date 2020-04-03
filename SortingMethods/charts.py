import numpy as np
import matplotlib.pyplot as plt
import quickSort as qs
import mergeSort as ms
import timeit
import sortingTests as check
import random
import selectionSort
import insertSort
import copy

arrayOfTimeQs = []
arrayOfTimeMs = []
arrayOfTimeIs = []
arrayOfTimeSs = []

minRandomNumberInArray = 0
maxRandomNumberInArray = 10000
randomArraySize = 1000
howManyArraysToSort = 25

def quickSortCase(arr):
    start = timeit.default_timer()
    qs.quickSortArr(arr)
    end = timeit.default_timer()
    
    time = end - start

    print("QuickSort arr: ")
    print(arr)
    print("Time: " + str(time))


    arrayOfTimeQs.append(time)

def mergeSortCase(arr):
    start = timeit.default_timer()
    ms.mergeSort(arr)
    end = timeit.default_timer()
    
    time = end - start

    print("MergeSort arr: ")
    print(arr)
    print("Time: " + str(time))

    arrayOfTimeMs.append(time)

def selectionSortCase(arr):
    start = timeit.default_timer()
    selectionSort.selectionSort(arr)
    end = timeit.default_timer()
    
    time = end - start

    print("Selection sort arr: ")
    print(arr)
    print("Time: " + str(time))

    arrayOfTimeSs.append(time)

def insertionSortCase(arr):
    start = timeit.default_timer()
    insertSort.insertionSort(arr)
    end = timeit.default_timer()
    
    time = end - start

    print("InserionSort arr: ")
    print(arr)
    print("Time: " + str(time))

    arrayOfTimeIs.append(time)

def sortArraysToCalculateTime():
    arrayOfTimeQs = []
    arrayOfTimeMs = []
    arrayOfTimeSs = []
    arrayOfTimeIs = []

    for i in range(0, howManyArraysToSort):
        array_qs = np.random.randint(low = minRandomNumberInArray, high = maxRandomNumberInArray, size = randomArraySize) 
        array_ms = copy.copy(array_qs)
        array_ss = copy.copy(array_qs)
        array_is = copy.copy(array_qs)

        mergeSortCase(array_ms)
        selectionSortCase(array_ss)
        insertionSortCase(array_is)
        quickSortCase(array_qs)

        print("Arrays to sort left: " + str(howManyArraysToSort - i - 1))
        if not check.areArraysEqual(array_qs, array_ms) and not check.areArraysEqual(array_ss, array_is): 
            print("SORTING FAILED, ARRAYS NOT EQUAL")
            break


def showChartsOfTime(titleOfChart):
    fig = plt.figure()
    fig.suptitle(titleOfChart)

    plt.plot(arrayOfTimeQs, label='QuickSort')
    plt.plot(arrayOfTimeMs,  label= 'MergeSort')
    plt.plot(arrayOfTimeSs, label= 'SelectionSort')
    plt.plot(arrayOfTimeIs, label= 'InsertionSort')

    plt.xlabel('Index of sorted Array')
    plt.ylabel('Time in seconds')

    plt.legend()
    plt.show()

  
