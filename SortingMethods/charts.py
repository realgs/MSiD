import numpy as np
import matplotlib.pyplot as plt
from SortingMethods import quickSort as qs
import timeit as time

arrayOfTime = []
maxRandomNumberInArray = 10000
randomArraySize = 100

for i in range(0, 100):
    array = np.random.randint(maxRandomNumberInArray, randomArraySize)
    start = time.start
    quickSortArr(array)
    end = time.end

    arrayOfTime.append(end - start)


for i in range(0, len(arrayOfTime)):
    print(i)

#fig, ax = plt.subplots()
#ax.plot(len(arrayOfTime), arrayOfTime)