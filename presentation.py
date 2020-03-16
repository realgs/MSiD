import random
from bubbleSort import bubbleSort
from insertSort import insertSort

testTab = [random.randint(-100,100) for i in range(15)]
print("Before bubble sort sort:")
print(testTab)
bubbleSort(testTab)
print("After bubble sort sort:")
print(testTab)

testTab = [random.randint(-100,100) for i in range(15)]
print("Before insert sort sort:")
print(testTab)
insertSort(testTab)
print("After insert sort sort:")
print(testTab)