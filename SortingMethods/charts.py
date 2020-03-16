import numpy as np
import matplotlib.pyplot as plt
import quickSort as qs
import mergeSort as ms
import timeit

arrayOfTimeQs = []
arrayOfTimeMs = []

maxRandomNumberInArray = 10000
randomArraySize = 10000
howManyArraysToSort = 100

for i in range(0, howManyArraysToSort):
    array_qs = np.random.randint(low = 0, high = maxRandomNumberInArray, size = randomArraySize) 
    array_ms = array_qs.copy()

    start = timeit.default_timer()
    qs.quickSortArr(array_qs)
    end = timeit.default_timer()

    arrayOfTimeQs.append(end - start)
    
    start = timeit.default_timer()
    ms.mergeSort(array_ms)
    end = timeit.default_timer()

    arrayOfTimeMs.append(end - start)


fig = plt.figure()
fig.suptitle("Time of sorting arrays")

plt.plot(arrayOfTimeQs, label='QuickSort')
plt.plot(arrayOfTimeMs,  label= 'MergeSort')

plt.xlabel('Index of sorted Array')
plt.ylabel('Time')

plt.legend()

plt.show()