import time


# measures run time of a function

def measure_time(function):
    start_time = time.time()
    function()
    return time.time() - start_time
