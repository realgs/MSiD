import time
from sys import float_info

def measureTime(function, array):
    startTime = time.time()
    function(array)
    return time.time()-startTime

def compareAll(functions, array):
    bestFunction = None
    bestTime = float_info.max
    for f in functions:
        tmpArray = array.copy()
        print(f"\nRunning {f.__name__}")
        executionTime = measureTime(f, tmpArray)
        print(f"Executed in: {executionTime:0.6f}s")
        if executionTime < bestTime:
            bestTime = executionTime
            bestFunction = f
    print(f"This time {bestFunction.__name__} was the fastest, sorting the array in just {bestTime:0.6f}s!")
