
def bubbleSort(inputTab):
    for lap in range(len(inputTab)-1,0,-1):
        for i in range(lap):
            if inputTab[i] > inputTab[i+1]:
                inputTab[i],inputTab[i+1] = inputTab[i+1], inputTab[i]