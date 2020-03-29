import random
from bubbleSort import bubbleSort
from insertSort import insertSort
from selectSort import selectSort
from quickSort import quicksort

testTab = [random.randint(-100,100) for i in range(5)]
print("Before bubble sort sort:")
print(testTab)
bubbleSort(testTab)
print("After bubble sort sort:")
print(testTab)

testTab = [random.randint(-100,100) for i in range(5)]
print("Before insert sort sort:")
print(testTab)
insertSort(testTab)
print("After insert sort sort:")
print(testTab)

testTab = [random.randint(-100,100) for i in range(5)]
print("Before select sort sort:")
print(testTab)
selectSort(testTab)
print("After select sort sort:")
print(testTab)

testTab = [random.randint(-100,100) for i in range(5)]
print("Before quick sort sort:")
print(testTab)
quicksort(testTab)
print("After quick sort sort:")
print(testTab)