def merge_sort(sequence):
    """
    Sequence of numbers is taken as input, and is split into two halves, following which they are recursively sorted.
    """
    if len(sequence) < 2:
        return sequence

    mid = len(sequence) // 2     # note: 7//2 = 3, whereas 7/2 = 3.5

    left_sequence = merge_sort(sequence[:mid])
    right_sequence = merge_sort(sequence[mid:])

    return merge(left_sequence, right_sequence)

def merge(left, right):
    """
    Traverse both sorted sub-arrays (left and right), and populate the result array
    """
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]

    return result

array = [5,2,6,8,5,8,1]

print (merge_sort(array))