import requests
import matplotlib.pyplot
from datetime import datetime
import time
import random

#apiCurrencies = ['BTCUSDT', 'ETHBTC', 'LTCBTC']

INPUT_LENGTH = 5
SSS = 200 #Single Simulation Steps
SA = 5 #Simulation amount(how many simulations will be done)
START_DATE = '2019-11-01'
END_DATE = '2020-02-01'
RESULTS_AMOUNT = 4
RANDOM_MODIFIER = 0.0000001

def getData(startDate, endDate, symbol, delta=3600000):
    sTimeStamp = time.mktime(datetime.strptime(startDate,"%Y-%m-%d").timetuple())*1000
    eTimeStamp = time.mktime(datetime.strptime(endDate, "%Y-%m-%d").timetuple())*1000
    deltaTimeStamp = delta*999
    data = []
    previousTimeStamp = sTimeStamp
    for i in range(int(eTimeStamp-sTimeStamp)//deltaTimeStamp):
        currentTimeStamp = sTimeStamp+(i+1)*deltaTimeStamp
        request = requests.get('https://api.binance.com/api/v3/klines',
            params={'symbol':symbol,'interval':'1h','startTime':str(int(previousTimeStamp)),'endTime':str(int(currentTimeStamp)),'limit':'1000'})
        previousTimeStamp = currentTimeStamp
        data= data + request.json()

    request = requests.get('https://api.binance.com/api/v3/klines',
            params={'symbol': symbol, 'interval': '1h', 'startTime': str(int(previousTimeStamp)),'endTime': str(int(currentTimeStamp)), 'limit': '1000'})
    data = data + request.json()
    return data

def shiftData(data):
    calculated = []
    for d in data:
        changedData = []
        changedData.append(int(d[0]))
        changedData.append((float(d[4]) - float(d[1])) / float(d[4]))
        changedData.append(float(d[4]))
        changedData.append(float(d[5]))
        calculated.append(changedData)
# i[0] - open time, i[1] - % daily change, i[2] - close value, i[3] - volume
    return calculated

# Here I came across an idea, that in order to check "correctness" of simulation,
# I can print both simulation and real data for simulating period
# (Data used for learning do not include stock values for simulatig period

def deviationCalculation(givenData,learnData):
    exchange = 0.000000000001
    volume = 0.000000000001
    for i in range(len(givenData)):
        exchange += pow(learnData[i][1] - givenData[i][0],2)
        volume += pow(learnData[i][3] - givenData[i][1],2)
    overallDeviation = exchange*volume
    return[exchange, volume, overallDeviation]

def estimate(givenInterval, learningData):
    deviation= []

    for calculatingIntervalNum in range(len(learningData) - len(givenInterval) - 1):
        deviation.append([calculatingIntervalNum + len(givenInterval),
             deviationCalculation(givenInterval,
                learningData[calculatingIntervalNum:calculatingIntervalNum + len(givenInterval)])])
#looking for best results
    for i in range(RESULTS_AMOUNT):
        min_idx = i
        for j in range(i+1, len(deviation)):
            if deviation[min_idx][1][2] > deviation[j][1][2]:
                min_idx = j
        deviation[i], deviation[min_idx] = deviation[min_idx], deviation[i]

    return calculateEstimation(deviation[:RESULTS_AMOUNT], learningData)

def calculateEstimation(bestMatchedResults, systemData):
    excSum = posEstimate = corSum = volSum = 0
    for resultIndex, deviations in bestMatchedResults:
        correctness = (1-random.uniform(-RANDOM_MODIFIER, RANDOM_MODIFIER))/deviations[0]
        corSum += correctness
        excSum += correctness * systemData[resultIndex][1]
        volSum += correctness * systemData[resultIndex][2]
        if systemData[resultIndex][1] > 0:
            posEstimate += correctness
    return [excSum/corSum, posEstimate/corSum, volSum/corSum, corSum]

def calculateAverageResults():
    averageResults = []
    for stepIndex in range(SSS):
        averageOfStep = 0
        for simulationIndex in range(SA):
            #print(stepIndex, simulationIndex)
            averageOfStep += simulationResults[simulationIndex][stepIndex]
        averageOfStep = averageOfStep/SA
        averageResults.append(averageOfStep)
    return averageResults


print("bip")
#print(getData(START_DATE,END_DATE,'BTCUSDT')  )
data = getData(START_DATE,END_DATE,'ETHBTC')

shiftedData = shiftData(data)
learnData = shiftedData[:len(data)-SSS]

inputs = [[learnData[i][1],learnData[i][3]]for i in range(len(learnData))]

calcData = [learnData[i][2] for i in range(len(learnData))]
realData = [shiftedData[i][2] for i in range(len(shiftedData))]

#simulation
simulationResults = []
volumes = []
for simulationIndex in range(SA):
    print("Simulation number {}".format(simulationIndex+1))
    inputs = [[learnData[i][1],learnData[i][3]]for i in range(len(learnData))]
    calcData = [learnData[i][2] for i in range(len(learnData))]

    for i in range(SSS):
        givenRequest = inputs[-INPUT_LENGTH :]
        estimatedChange, positiveChangeChance, estimatedVolume, qualityOfEstimate = estimate(givenRequest, learnData)
        volumes.append(estimatedVolume)
        inputs.append([estimatedChange, estimatedVolume])
        calcData.append(estimatedChange*calcData[-1]+calcData[-1])
    simulationResults.append(calcData[-SSS:])

simulation = calculateAverageResults()

#Plot
domain1 = [x for x in range(len(realData)-SSS,len(realData))]
domain2 = [x for x in range(len(realData))]
domain3 = [x for x in range(len(realData)-SSS,len(realData))]
matplotlib.pyplot.plot(domain1, simulation, label = "Average simulation")
matplotlib.pyplot.plot(domain2, realData,label ="Real data")
matplotlib.pyplot.plot(domain3, simulationResults[1], label = "single simulation")
print("boop - gotowe")
matplotlib.pyplot.legend()
matplotlib.pyplot.show()