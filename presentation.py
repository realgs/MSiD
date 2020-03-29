import random
import time
import copy
from bubbleSort import bubbleSort
from insertSort import insertSort
from selectSort import selectSort
from quickSort import quickSort

def measureTime(sortFunctions, tabSize):
    testTab = [random.randint(-100,100) for i in range(tabSize)]
    results = {}
    for sortFunc in sortFunctions:
        tab = copy.copy(testTab)

        start = time.time()
        sortFunc(tab)
        end = time.time()

        if tab != sorted(tab):
            print("Your algorithm is wrong!")
            results[sortFunc] = -1
        else:
            results[sortFunc] = end-start
    return results


sortFunctions = [bubbleSort, insertSort, selectSort, quickSort]

result = measureTime(sortFunctions, 25000)

sortedResult = sorted(result, key=lambda x : result[x])
for sortFun in sortedResult:
    print("{} with time = {}".format(sortFun.__name__,result[sortFun]))