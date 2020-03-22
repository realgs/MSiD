def insert_sort(array):
    for i in range(len(array)):
        value = array[i]
        j = i
        while(j>0 and array[j-1] > value):
            array[j] = array[j-1]
            j-=1
        array[j] = value

numbers = [234, 4, -2, 15, 9, -30, 999]
insert_sort(numbers)
print(numbers)
