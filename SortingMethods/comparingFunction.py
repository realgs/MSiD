import insertSort 
import mergeSort
import selectionSort
import quickSort
import time 
from random import randint
import sys

def compareFunctions(diffrentSortingFunctions, arrayToSort):
    bestTime = sys.float_info.max
    bestFunction = None

    for function in diffrentSortingFunctions:
        copy_array = arrayToSort[:]
        start = time.time()
        function(copy_array)
        end = time.time()
        result = end - start
        if bestTime > result:
            bestTime = result
            bestFunction = function
        print("Funkcja: " + function.__name__ + ". Czas sortowania wynosi:" + str(result))


    print("Najlepsza funkcja sortujaca ta tablice to: " + bestFunction.__name__ + ". Czas sortowania wynosi:" + str(bestTime))

def main():
    array = [randint(0, 100) for _ in range(0, 10000)]
    functions = [insertSort.insertionSort, mergeSort.mergeSort, selectionSort.selectionSort, quickSort.quickSortArr]

    compareFunctions(functions, array)

main()


