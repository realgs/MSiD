import sorts
import timeit
from BinarySearchTree import BST
from random import shuffle, randint
from dill.source import getname


def compare(func, list_to_sort):
    if func == sorts.pancake_sort or func == sorts.tree_sort:
        start_time = timeit.default_timer()
        func(list_to_sort)
        print(getname(func), "Result: ", timeit.default_timer() - start_time, "s")
    elif func == sorts.quick_sort:
        start_time = timeit.default_timer()
        func(list_to_sort, 0, len(list_to_sort)-1)
        print(getname(func), "Result: ", timeit.default_timer() - start_time, "s")
    else:
        start_time = timeit.default_timer()
        func(list_to_sort, 0, len(list_to_sort))
        print(getname(func), "Result: ", timeit.default_timer() - start_time, "s")


def functionTest(test_list):
    print()
    shuffle(test_list)
    compare(sorts.quick_sort, test_list)
    shuffle(test_list)
    compare(sorts.insertion_sort, test_list)
    shuffle(test_list)
    compare(sorts.tree_sort, test_list)
    shuffle(test_list)
    compare(sorts.pancake_sort, test_list)


def main():
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
    print()

    realnumber_list = list(range(-5000, 5000))
    realnumber_list = [i / randint(2, 9) for i in realnumber_list]
    shuffle(realnumber_list)
    functionTest(realnumber_list)
    shuffled_list = list(range(10000))
    shuffle(shuffled_list)
    functionTest(shuffled_list)
    integer_list = list(range(-10000, 10000))
    shuffle(integer_list)
    functionTest(integer_list)


if __name__ == "__main__":
    main()