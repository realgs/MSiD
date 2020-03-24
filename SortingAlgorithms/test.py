import sorts
from BinarySearchTree import BST
from random import shuffle


def main():
    # test_list = list(range(-50, 50))
    test_list = [-2.3, 1, 3, 4.2, 4, 2.4, -5.2, 10.9, 11, 3.9]
    shuffle(test_list)
    print("List to sort: ", test_list)
    sorts.insertion_sort(test_list, 0, len(test_list))
    print("\nSorted list by Insertion Sort: ", test_list)
    shuffle(test_list)
    print("\nNew list to sort: ", test_list)
    sorts.quick_sort(test_list, 0, len(test_list) - 1)
    print("\nSorted list by Quick Sort: ", test_list)
    shuffle(test_list)
    print("\nNew list to sort: ", test_list)
    print("\nSorted list by Tree Sort: ", sorts.tree_sort(test_list))
    shuffle(test_list)
    print("\nNew list to sort: ", test_list)
    sorts.pancake_sort(test_list)
    print("\nSorted list by Pancake Sort: ", test_list)


if __name__ == "__main__":
    main()