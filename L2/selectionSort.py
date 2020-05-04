def selectionSort(array):
    for i in range(len(array)): 
        miniIdx = i 
        for j in range(i+1, len(array)): 
            if array[miniIdx] > array[j]: 
               miniIdx = j 
        array[i], array[miniIdx] = array[miniIdx], array[i]