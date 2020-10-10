

def bubble_sort(array):
    length = len(array);
    for i in range(length):
        for j in range(length - i - 1):
            if array[j] > array[j+1]:
                 array[j], array[j+1] = array[j+1], array[j]

def merge_sort(array):
    def merge(array, left, right):
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                array[k] = left[i]
                i+=1
            else:
                array[k] = right[j]
                j+=1
            k+=1

        while i < len(left):
            array[k] = left[i]
            i+=1
            k+=1

        while j < len(right):
            array[k] = right[j]
            j+=1
            k+=1

    def merge_sort_helper(array):
        if len(array) > 1:
            mid = len(array) // 2
            left = array[:mid]
            right = array[mid:]
            merge_sort_helper(left)
            merge_sort_helper(right)
            merge(array, left, right)

    merge_sort_helper(array)

def main():
    arr = [-7,2,19,3,2,0,-51,-3,12]
    arr2 = arr[:]
    print(arr, "\n")

    bubble_sort(arr)
    print(arr)

    merge_sort(arr2)
    print(arr2)

if __name__ == "__main__":
    main()
