
def insertSort(inputTab):
    for lap in range(1,len(inputTab)):
        for i in range(lap,0,-1):
            if inputTab[i] < inputTab[i-1]:
                inputTab[i-1],inputTab[i] = inputTab[i], inputTab[i-1]
            else:
                break
