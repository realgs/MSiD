import copy

def recursiveQuick(inputTab):
    if len(inputTab) < 2:
        return inputTab
    else:
        pivot = inputTab[0]
        less = [i for i in inputTab[1:] if i <= pivot]
        greater = [i for i in inputTab[1:] if i > pivot]
        return recursiveQuick(less) + [pivot] + recursiveQuick(greater)



def quicksort(inputTab):
    inputTab[:] = recursiveQuick(inputTab)