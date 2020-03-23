from random import shuffle


def insertion_sort(list_to_sort):
    if len(list_to_sort) <= 0:
        return
    for i in range(1, len(list_to_sort)):
        elem_to_insert = list_to_sort[i]
        j = i - 1
        while j >= 0 and list_to_sort[j] > elem_to_insert:
            list_to_sort[j + 1] = list_to_sort[j]
            j -= 1
        list_to_sort[j + 1] = elem_to_insert
    return list_to_sort


def main():
    test_list = list(range(100))
    shuffle(test_list)
    print("List to sort: ", test_list)
    print("\nSorted list: ", insertion_sort(test_list))
    # print(insertion_sort(test_list))


if __name__ == "__main__":
    main()
