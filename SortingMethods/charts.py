import numpy as np
import matplotlib.pyplot as plt
import quickSort as qs
import mergeSort
import timeit
import sortingTests as check
import random
import selectionSort
import insertSort
import copy
from random import randint

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
    mergeSort.mergeSort(arr)
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
        array_qs = [randint(minRandomNumberInArray, maxRandomNumberInArray) for _ in range(0, randomArraySize)]
        array_ms = copy.copy(array_qs)
        array_ss = copy.copy(array_qs)
        array_is = copy.copy(array_qs)

        mergeSortCase(array_ms)
        selectionSortCase(array_ss)
        insertionSortCase(array_is)
        quickSortCase(array_qs)

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

  
