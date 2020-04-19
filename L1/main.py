import insertSort
import mergeSort

array_is = [1,6,32,1,3,2,56,7,8,2]
array_ms = array_is[:]

insertSort.insertionSort(array_is)
mergeSort.mergeSort(array_ms)

print(array_is)
print(array_ms)