from random import shuffle, randint
from BinarySearchTree import BST as tr


def quick_sort(list_to_sort, low, high):
    if low < high:
        pi = partition(list_to_sort, low, high)
        if high - low < 10:
            insertion_sort(list_to_sort, low, high+1)
            low = high
        else:
            quick_sort(list_to_sort, low, pi-1)
            quick_sort(list_to_sort, pi+1, high)


def partition(li_sort, low, high):
    piv_pos = randint(low, high)     # picking random element as pivot
    pivot = li_sort[piv_pos]
    li_sort[piv_pos], li_sort[high] = li_sort[high], li_sort[piv_pos]
    i = (low-1)
    for j in range(low, high):
        if li_sort[j] < pivot:
            i += 1
            li_sort[i], li_sort[j] = li_sort[j], li_sort[i]
    li_sort[i + 1], li_sort[high] = li_sort[high], li_sort[i + 1]
    return i + 1


def insertion_sort(list_to_sort, low, high):
    if len(list_to_sort) <= 0:
        return
    for i in range(low+1, high):
        elem_to_insert = list_to_sort[i]
        j = i - 1
        while j >= 0 and list_to_sort[j] > elem_to_insert:
            list_to_sort[j + 1] = list_to_sort[j]
            j -= 1
        list_to_sort[j + 1] = elem_to_insert
    # return list_to_sort


def tree_sort(li_sort):
    root = tr.Node(li_sort[0])
    for i in range(1, len(li_sort)):
        tr.insert(root, tr.Node(li_sort[i]))
    li_sort = []
    inOrderTraversal(root, li_sort)
    return li_sort


def inOrderTraversal(root, result_list):
    if root:
        inOrderTraversal(root.l_child, result_list)
        result_list.append(root.data)
        inOrderTraversal(root.r_child, result_list)


def flip(li_sort, i):
    start = 0
    while start < i:
        li_sort[start], li_sort[i] = li_sort[i], li_sort[start]
        start += 1
        i -= 1


def findMaxIndex(li_sort, list_len):
    max_index = 0
    for i in range(1, list_len):
        if li_sort[i] > li_sort[max_index]:
            max_index = i
    return max_index


def pancake_sort(li_sort):
    size = len(li_sort)
    while size > 1:
        max_index = findMaxIndex(li_sort, size)
        if max_index != size-1:
            flip(li_sort, max_index)
            flip(li_sort, size-1)
        size -= 1