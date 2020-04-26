def shell_sort(array):
    #generate gaps distances using Papernov & Stasevich sequence
    def generate_gaps_ps():
        gaps = [1]
        gap = 1
        while gap < len(array)//3:
            gap = gap*2
            gaps.insert(0, gap+1)
        return gaps

    def shell_sort_helper(array, gaps):
        for gap in gaps:
            for i in range(gap, len(array)):
                temp = array[i]
                j = i
                while  j >= gap and array[j-gap] > temp:
                    array[j] = array[j-gap]
                    j -= gap
                array[j] = temp

    shell_sort_helper(array, generate_gaps_ps())

def quick_sort(array):
    def quick_sort_helper(array, low, high):
        if(low >= high):
            return
        left, right = low, high
        pivot = array[(left + right) // 2]

        while left <= right:
            while array[left] < pivot:
                left+=1
            while array[right] > pivot:
                right-=1
            if left <= right:
                array[left], array[right] = array[right], array[left]
                left+=1
                right-=1

        quick_sort_helper(array, low, right)
        quick_sort_helper(array, left, high)

    quick_sort_helper(array, 0, len(array)-1)

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
