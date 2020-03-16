import random
from bubbleSort import bubbleSort


testTab = [random.randint(-100,100) for i in range(15)]
print(testTab)
bubbleSort(testTab)
print(testTab)
