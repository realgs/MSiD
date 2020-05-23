from random import shuffle, randint


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


def main():
    test_list = list(range(100))
    shuffle(test_list)
    print("List to sort: ", test_list)
    insertion_sort(test_list, 0, len(test_list))
    print("\nSorted list by Insertion Sort: ", test_list)
    # print(insertion_sort(test_list))
    shuffle(test_list)
    print("\nNew list to sort: ", test_list)
    quick_sort(test_list, 0, len(test_list) - 1)
    print("\nSorted list by Quick Sort: ", test_list)


if __name__ == "__main__":
    main()
