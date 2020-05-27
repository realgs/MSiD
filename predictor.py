import requests
import matplotlib.pyplot as plt
from datetime import datetime
import time
import random

PREDICTION_RANDOM_MAX_MODIFICATOR = 0.007
HOW_MANY_BEST_RESULTS = 3
INPUT_SIZE = 5
STEPS_OF_SIMULATION = 300
NUMBER_OF_SIMULATIONS = 250
START = '2019-12-01'
END = '2020-02-01'
SHOW_SUB_SIMULATIONS = True


def downloadData(start, end, granularity = 3600000):
    startTimeStamp = time.mktime(datetime.strptime(start, "%Y-%m-%d").timetuple())
    endTimeStamp = time.mktime(datetime.strptime(end, "%Y-%m-%d").timetuple())
    startTimeStamp *= 1000
    endTimeStamp *= 1000
    timestampStep = granularity*999
    #All this stuf is needed because of API limitations :c
    rawData = []
    startStamp = startTimeStamp
    for i in range(int(endTimeStamp-startTimeStamp)//timestampStep):
        endStamp = startTimeStamp+(i+1)*timestampStep
        r = requests.get('https://api.binance.com/api/v3/klines',
            params={'symbol':'BTCUSDT','interval':'1h','startTime':str(int(startStamp)),'endTime':str(int(endStamp)),'limit':'1000'})
        startStamp = endStamp
        rawData = rawData+r.json()

    r = requests.get('https://api.binance.com/api/v3/klines',
            params={'symbol':'BTCUSDT','interval':'1h','startTime':str(int(startStamp)),'endTime':str(int(endTimeStamp)),'limit':'1000'})
    rawData = rawData+r.json()
    return rawData

#parse data to [timestamp, percent change between open and close, close value, volume]
def parseDataAndCalculateChanges(dataSet):
    parsedData = []
    for d in dataSet:
        setOfDataWithChanges = []
        setOfDataWithChanges.append(int(d[0]))                              #Open time
        setOfDataWithChanges.append((float(d[4])-float(d[1]))/float(d[4]))  #Daily change
        setOfDataWithChanges.append(float(d[4]))                            #Close value
        setOfDataWithChanges.append(float(d[5]))                            #Volume
        parsedData.append(setOfDataWithChanges)
    return parsedData


def calculateDeviation(givenData, systemData):
    exchangeDeviation = 0.000000000001
    volumeDeviation = 0.000000000001
    for dataIndex in range(len(givenData)):
        exchangeDeviation += pow(systemData[dataIndex][1] - givenData[dataIndex][0],2)
        volumeDeviation += pow(systemData[dataIndex][3] - givenData[dataIndex][1],2)
    generalDeviation = exchangeDeviation*volumeDeviation
    return [exchangeDeviation, volumeDeviation, generalDeviation]


def calculateEstimatedValues(bestMatchedResults, systemData):
    ExchangechangeSum = 0.0
    deviationSum = 0.0
    positiveEstimate = 0.0
    correctnessSum = 0.0
    volumeSum = 0.0
    for resultIndex, deviations in bestMatchedResults:
        correctness = (1-random.uniform(-PREDICTION_RANDOM_MAX_MODIFICATOR, PREDICTION_RANDOM_MAX_MODIFICATOR))/deviations[0]
        correctnessSum += correctness
        ExchangechangeSum += correctness * systemData[resultIndex][1]
        volumeSum += correctness * systemData[resultIndex][2]
        if systemData[resultIndex][1] > 0:
            positiveEstimate += correctness

    weightAverageOfChange = ExchangechangeSum/correctnessSum
    positiveChance = positiveEstimate/correctnessSum
    weightAverageOfVolume = volumeSum/correctnessSum

    return [weightAverageOfChange, positiveChance, weightAverageOfVolume, correctnessSum]


def getBestApprox(deviationMap):
    for i in range(HOW_MANY_BEST_RESULTS):
        min_idx = i
        for j in range(i+1, len(deviationMap)):
            if deviationMap[min_idx][1][2] > deviationMap[j][1][2]:
                min_idx = j
        deviationMap[i], deviationMap[min_idx] = deviationMap[min_idx], deviationMap[i]

    return deviationMap[:HOW_MANY_BEST_RESULTS]


def estimate(givenInterval, systemData):
    deviationMap = []
    for calculatingIntervalNum in range(len(systemData) - len(givenInterval) -1):
        deviationMap.append([calculatingIntervalNum+len(givenInterval),
           calculateDeviation(givenInterval,
              systemData[calculatingIntervalNum:calculatingIntervalNum+len(givenInterval)])])
    bestApprox = getBestApprox(deviationMap)
    return calculateEstimatedValues(bestApprox, systemData)


def calculateAverageValues(simulationsData):
    averageResultsFromSimulation = []
    for stepIndex in range(STEPS_OF_SIMULATION):
        averageOfStep = 0
        for simulationIndex in range(NUMBER_OF_SIMULATIONS):
            averageOfStep += simulationResults[simulationIndex][stepIndex]
        averageOfStep = averageOfStep/NUMBER_OF_SIMULATIONS
        averageResultsFromSimulation.append(averageOfStep)
    return averageResultsFromSimulation

rawData = downloadData(START,END)

parsedInternetDataAll = parseDataAndCalculateChanges(rawData)
parsedInternetDataForLearn = parsedInternetDataAll[:len(rawData)-STEPS_OF_SIMULATION]

inputsForCalcs = [[parsedInternetDataForLearn[i][1],parsedInternetDataForLearn[i][3]]for i in range(len(parsedInternetDataForLearn))]

calcData = [parsedInternetDataForLearn[i][2] for i in range(len(parsedInternetDataForLearn))]
realData = [parsedInternetDataAll[i][2] for i in range(len(parsedInternetDataAll))]

simulationResults = []
for simulationIndex in range(NUMBER_OF_SIMULATIONS):
    print("Okrążenie {}".format(simulationIndex+1))
    inputsForCalcs = [[parsedInternetDataForLearn[i][1],parsedInternetDataForLearn[i][3]]for i in range(len(parsedInternetDataForLearn))]
    calcData = [parsedInternetDataForLearn[i][2] for i in range(len(parsedInternetDataForLearn))]

    for i in range(STEPS_OF_SIMULATION):
        givenRequest = inputsForCalcs[-INPUT_SIZE:]

        estimatedChange, positiveChangeChance, estimatedVolume, qualityOfEstimate = estimate(givenRequest, parsedInternetDataForLearn)
        
        inputsForCalcs.append([estimatedChange, estimatedVolume])
        calcData.append(estimatedChange*calcData[-1]+calcData[-1])

    simulationResults.append(calcData[-STEPS_OF_SIMULATION:])




averageResultsFromSimulation = calculateAverageValues(simulationResults)

domain1 = [x for x in range(len(realData)-STEPS_OF_SIMULATION,len(realData))]
domain2 = [x for x in range(len(realData))]

if SHOW_SUB_SIMULATIONS:
    for i in range(len(simulationResults)):
        plt.plot(domain1, simulationResults[i],label =str(i))

plt.plot(domain1, averageResultsFromSimulation, label = "Average")
plt.plot(domain2, realData,label ="Real data")

plt.legend()
plt.show()
