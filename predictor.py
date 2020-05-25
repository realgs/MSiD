import requests
import matplotlib.pyplot as plt
from datetime import datetime

DAYS_BEFORE = 5
HOW_MANY_BEST_RESULTS = 10

#parse data to [timestamp, percent change between open and close, close value, volume]
def parseDataAndCalculateChanges(dataSet):
    parsedData = []
    for d in dataSet:
        setOfDataWithChanges = []
        setOfDataWithChanges.append(d[0])
        setOfDataWithChanges.append((d[4]-d[3])/d[4])
        setOfDataWithChanges.append(d[4])
        setOfDataWithChanges.append(d[5])
        parsedData.append(setOfDataWithChanges)
    return parsedData

def calculateDeviation(givenData, systemData):
    deviation = 0.000000000001
    for dataIndex in range(len(givenData)):
        deviation += pow(systemData[dataIndex][1]-givenData[dataIndex],2)
    return deviation

def calculateEstimatedValues(bestMatchedResults, realData):
    changeSum = 0
    devSum = 0
    positiveEstimate = 0
    for resultIndex, deviation in bestMatchedResults:
        print(realData[resultIndex][1])
        correctness = 1/deviation
        print("Correctness = {} for result {}".format(correctness,realData[resultIndex][1]))
        changeSum += correctness * realData[resultIndex][1]
        devSum += correctness
        if realData[resultIndex][1] > 0:
            positiveEstimate += correctness

    weightAverageOfChange = changeSum/devSum
    positiveChance = positiveEstimate/devSum
    return [weightAverageOfChange,positiveChance]



r = requests.get('https://api-public.sandbox.pro.coinbase.com/products/BTC-USD/candles',
    params={'start':'2019-09-01','end':'2020-03-01','granularity':'86400'})
rawData = r.json()

dataWithChanges = parseDataAndCalculateChanges(rawData)
givenRequest = [dataWithChanges[130][1], dataWithChanges[131][1],
 dataWithChanges[132][1], dataWithChanges[133][1], dataWithChanges[134][1]]

deviationMap = []
for calculatingIntervalNum in range(len(dataWithChanges) - DAYS_BEFORE -1):
    deviationMap.append([calculatingIntervalNum+DAYS_BEFORE+1,
      calculateDeviation(givenRequest,
      dataWithChanges[calculatingIntervalNum:calculatingIntervalNum+DAYS_BEFORE])])

bestResults = sorted(deviationMap, key=lambda x:x[1])[:HOW_MANY_BEST_RESULTS]

estimatedChange, positiveChangeChance = calculateEstimatedValues(bestResults,dataWithChanges)


print("Prawdopodobna zmiana:")
print(estimatedChange)
print("Szansa na + {}%".format(positiveChangeChance*100))
print("Szansa na - {}%".format((1-positiveChangeChance)*100))
print(dataWithChanges[135])

