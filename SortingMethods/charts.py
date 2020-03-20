import numpy as np
import matplotlib.pyplot as plt
import quickSort as qs
import mergeSort as ms
import timeit
import sortingTests as check
import random

arrayOfTimeQs = []
arrayOfTimeMs = []

minRandomNumberInArray = 0
maxRandomNumberInArray = 10000
randomArraySize = 100000
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

def sortArraysToCalculateTime():
    arrayOfTimeQs = []
    arrayOfTimeMs = []

    for i in range(0, howManyArraysToSort):
        array_qs = np.random.randint(low = minRandomNumberInArray, high = maxRandomNumberInArray, size = randomArraySize) 
        array_ms = array_qs[:]

        quickSortCase(array_qs)
        mergeSortCase(array_ms)
        print("Arrays to sort left: " + str(howManyArraysToSort - i - 1))
        if not check.areArraysEqual(array_qs, array_ms): 
            print("SORTING FAILED, ARRAYS NOT EQUAL")
            break


def showChartsOfTime(titleOfChart):
    fig = plt.figure()
    fig.suptitle(titleOfChart)

    plt.plot(arrayOfTimeQs, label='QuickSort')
    plt.plot(arrayOfTimeMs,  label= 'MergeSort')

    plt.xlabel('Index of sorted Array')
    plt.ylabel('Time in seconds')

    plt.legend()
    plt.show()

  
