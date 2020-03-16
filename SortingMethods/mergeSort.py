def mergeSort(array):
    if len(array) > 1:
        middle = len(array) // 2
  
        leftArr = array[:middle]
        rightArr = array[middle:]

        mergeSort(leftArr) 
        mergeSort(rightArr)

        merge(array, leftArr, rightArr)

def merge(array, leftArr, rightArr):
    i = 0
    j = 0

    k = 0

    while i < len(leftArr) and j < len(rightArr):
        if leftArr[i] < rightArr[j]:
            array[k] = leftArr[i]
            i += 1
        else:
            array[k] = rightArr[j]
            j += 1

        k += 1
    
    while i < len(leftArr):
        array[k] = leftArr[i]
        i += 1
        k += 1

    while j < len(rightArr):
        array[k] = rightArr[j]
        j += 1
        k += 1

myList = [54,26,93,17,77,31,44,55,20]
mergeSort(myList)
print(myList)