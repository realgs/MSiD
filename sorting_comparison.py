import timeit
import random
import string
from sorting_algorithms import *

def measure_execution_time(function, array):
    time_start = timeit.default_timer()
    function(array)
    time_end = timeit.default_timer()
    print("{0}: {1:.5f} s".format(function.__name__, (time_end - time_start) * 1000))

def compare_execution_time(functions, array):
    for function in functions:
        measure_execution_time(function, array[:])
    print

def compare_sorting_algorithms(array):
    functions = [merge_sort, quick_sort, bubble_sort, shell_sort]

    #check if functions sort properly
    array_sorted = array[:]
    array_sorted.sort()
    for function in functions:
        array_to_sort = array[:]
        function(array_to_sort)
        if array_to_sort != array_sorted:
            print("WARNING - {0}'S OUTPUT IS MISCALCULATED".format(function.__name__))


    print("RANDOM ORDER")
    compare_execution_time(functions, array)
    print("ASCENDING ORDER")
    array.sort()
    compare_execution_time(functions, array)
    print("DESCENDING ORDER")
    array.reverse()
    compare_execution_time(functions, array)

def main():
    print("- - - -\nINT\n- - - -")
    array_of_ints = random.sample(range(-10000, 10000), 1000)
    compare_sorting_algorithms(array_of_ints[:])

    print("- - - -\nSTRING\n- - - -")
    array_of_strings = [''.join(random.choice(string.ascii_uppercase) for _ in range(6)) for _ in range(1000)]
    compare_sorting_algorithms(array_of_strings[:])

if __name__ == "__main__":
    main()
