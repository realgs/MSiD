import time
import random


def measure_time(function):
    start_time = time.time()
    function()
    return time.time() - start_time


def benchmark_sorting_functions(functions):
    arr = [random.uniform(1, 10000) for _ in range(10000)]

    for function in functions:
        array = arr.copy()
        print(function.__name__ + ": " + str(measure_time(lambda: function(array))))
