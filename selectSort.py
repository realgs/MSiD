
def selectSort(inputTab):
    for i in range(len(inputTab)):
        minIndex = i
        for j in range(i,len(inputTab)):
            if inputTab[minIndex] > inputTab[j]:
                minIndex = j
        if minIndex != i:
            inputTab[i], inputTab[minIndex] = inputTab[minIndex], inputTab[i]


