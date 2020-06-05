import requests
import json
import time
from datetime import datetime, timedelta
import os
import csv
import sys
import numpy as np

markets = ("USD-BTC", "USD-ETH", "BTC-LTC", "USD-LTC")
markets_bitfinex = list('t' + market[4:] + market[:3] for market in markets)
markets_binance = list(market[4:] + market[:3] +'T' if market[:3] == 'USD' else market[4:] + market[:3] for market in markets)
markets_bitbay = list((market[4:]+'-'+market[:3] for market in markets))

MARKETS_NUM = 4
bittrexFee = 0.0025
bitbayFee = 0.0041
binanceFee = 0.001
bitfinexFee = 0.002

# 0 - USD-BTC
# 1 - USD-ETH
# 2 - BTC-LTC
# 3 - USD-LTC
bittrex_data = np.zeros(shape=(4,2))
binance_data = np.zeros(shape=(4,2))
bitfinex_data = np.zeros(shape=(4,2))
bitbay_data = np.zeros(shape=(4,2))

exchanges_data = [bittrex_data, binance_data, bitfinex_data, bitbay_data]
exchanges_labels = ['Bittrex', 'Binance', 'Bitfinex', 'Bitbay']

def cls(): os.system('cls' if os.name == 'nt' else 'clear')


def calculateDiff(sell_price, buy_price):
    if sell_price == None or buy_price == None:
        return -1
    return  (float(sell_price) - float(buy_price)) / float(buy_price)*100


def loadFromApiBittrex(market, market_number):
    url = 'https://api.bittrex.com/api/v1.1/public/getticker?market='+market
    response = requests.get(url)
    data = response.json()
    bittrex_data[market_number][0] = data['result']['Bid']
    bittrex_data[market_number][1] = data['result']['Ask']
    return data['result']['Bid'], data['result']['Ask']


def printDataBittrex(markets):
    data = []
    market_number = 0
    for market in markets:
        data.append(loadFromApiBittrex(market, market_number))
        market_number+=1
    output = "BITTREX\n"
    for i in range(len(markets)):
        diff = calculateDiff(data[i][1], data[i][0])
        output += ("Market: {0:15} Bid: {1:15}\tAsk: {2:15}Difference: {3:.2f} %\n".
            format(markets[i], str(data[i][0]), str(data[i][1]), diff))
    return output
    

def loadFromApiBinance(market, market_number):
    response = requests.get(f'https://api.binance.com/api/v3/depth?symbol={market}&limit=5')
    data = response.json()
    binance_data[market_number][0] = data['bids'][0][0]
    binance_data[market_number][1] = data['asks'][0][0]
    return data['bids'][0][0], data['asks'][0][0]


def printDataBinance(markets):
    data = []
    market_number = 0
    for market in markets_binance:
        data.append(loadFromApiBinance(market, market_number))
        market_number+=1
    output = "BINANCE\n"
    for i in range(len(markets)):
        diff = calculateDiff(data[i][1], data[i][0])
        output += ("Market: {0:15} Bid: {1:15}\tAsk: {2:15}Difference: {3:.2f} %\n".
            format(markets[i], str(data[i][0]), str(data[i][1]), diff))
    return output


def loadFromApiBitfinex(market, market_number):
    response = requests.get(f'https://api-pub.bitfinex.com/v2/book/{market}/P0?len=1')
    data = response.json()
    bitfinex_data[market_number][0] = data[0][0]
    bitfinex_data[market_number][1] = data[1][0]
    return data[1][0], data[0][0]


def printDataBitfinex(markets):
    data = []
    market_number = 0
    for market in markets_bitfinex:
        data.append(loadFromApiBitfinex(market, market_number))
        market_number+=1
    output = "BITFINEX\n"
    for i in range(len(markets)):
        diff = calculateDiff(data[i][0], data[i][1])
        output += ("Market: {0:15} Bid: {1:15}\tAsk: {2:15}Difference: {3:.2f} %\n".
            format(markets[i], str(data[i][1]), str(data[i][0]), diff))
    return output


def loadFromApiBitBay():
    url = 'https://api.bitbay.net/rest/trading/ticker'
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", url, headers=headers)
    response_dict = json.loads(response.text)
    for i in range(len(markets)):
        bitbay_data[i][0] = response_dict['items'][markets_bitbay[i]]['highestBid']
        bitbay_data[i][1] = response_dict['items'][markets_bitbay[i]]['lowestAsk']
    return response_dict


def printDataBitBay(markets):
    response_dict = loadFromApiBitBay()
    output = "BITBAY\n"
    for i in range(len(markets)):
            diff = calculateDiff(response_dict['items'][markets_bitbay[i]]['lowestAsk'], response_dict['items'][markets_bitbay[i]]['highestBid'])
            output += ("Market: {0:15} Bid: {1:15}\tAsk: {2:15}Difference: {3:.2f} %\n".
                format(markets[i], str(response_dict['items'][markets_bitbay[i]]['highestBid']), str(response_dict['items'][markets_bitbay[i]]['lowestAsk']), diff))
    return output



def trader(investedSum, taxesOn):
    while True:
        bestDeal = searchProfit(markets, investedSum, taxesOn)
        print(bestDeal)
        if bestDeal[-1] > investedSum: investedSum = bestDeal[-1]
        print("Money sum = ", bestDeal[-1])


def decreaseByFee(market, moneyAmount):
    if market == 'Bittrex':
        return moneyAmount - moneyAmount*bittrexFee
    elif market == 'Binance':
        return moneyAmount - moneyAmount*binanceFee
    elif market == 'Bitfinex':
        return moneyAmount - moneyAmount*bitfinexFee
    elif market == 'Bitbay':
        return moneyAmount - moneyAmount*bitbayFee
    else:
        print("Error")
        return -1
    


def searchProfit(markets, moneyAmount, taxesOn = True, specifiedIndex = -1):
    lowestAsk = [float('inf') for x in range(4)]
    highestBid = [-1*float('inf') for x in range(4)]
    askExchange = ['','','','']
    bidExchange = ['','','','']
    interval = timedelta(seconds=1)
    startTime = datetime.now()
    control_iter = 0

    while datetime.now() - startTime < interval:
        control_iter+=1
        for i in range(4):
            loadFromApiBinance(markets_binance[i], i)
            loadFromApiBitfinex(markets_bitfinex[i], i)
            loadFromApiBittrex(markets[i], i)
        loadFromApiBitBay()
        for market in range(len(markets)):
            for exchange in range(len(markets)):
                testAsk = exchanges_data[exchange][market][1].item()
                if testAsk < lowestAsk[market]:
                    lowestAsk[market] = testAsk
                    askExchange[market] = exchanges_labels[exchange]

    startTime = datetime.now()    
    control_iter = 0        
    while datetime.now() - startTime < interval:
        control_iter+=1
        for i in range(4):
            loadFromApiBinance(markets_binance[i], i)
            loadFromApiBitfinex(markets_bitfinex[i], i)
            loadFromApiBittrex(markets[i], i)
        loadFromApiBitBay()
        for market in range(len(markets)):
            for exchange in range(len(markets)):
                testBid = exchanges_data[exchange][market][0].item()
                if testBid > highestBid[market]:
                    highestBid[market] = testBid
                    bidExchange[market] = exchanges_labels[exchange]

    print(highestBid, "\t", lowestAsk)
    diff = [calculateDiff(highestBid[i], lowestAsk[i]) for i in range(4)]
    moneyAmount = [moneyAmount for i in range(4)]
    print("diff = ", diff)
    if specifiedIndex == -1:
        for i in range(4):
            if diff[i] > 0.0: 
                if markets[i] != "BTC-LTC":
                    if taxesOn: moneyAmount[i] = decreaseByFee(askExchange[i], moneyAmount[i])
                    currencyAmount = moneyAmount[i]/lowestAsk[i]
                    if taxesOn: currencyAmount = decreaseByFee(bidExchange[i], currencyAmount)
                    moneyAmount[i] = currencyAmount*highestBid[i]
                else:
                    moneyAmount[i] = moneyAmount[i]/(exchanges_data[1][0][1].item())
                    if taxesOn: moneyAmount[i] = decreaseByFee(askExchange[i], moneyAmount[i])
                    currencyAmount = moneyAmount[i]/lowestAsk[i]
                    if taxesOn: currencyAmount = decreaseByFee(bidExchange[i], currencyAmount)
                    moneyAmount[i] = currencyAmount*highestBid[i]*(exchanges_data[1][0][0].item())
                print(markets[i],"  Buy: ", askExchange[i], " - ", lowestAsk[i], "\tSell: ", bidExchange[i], " - ", highestBid[i],"\tDifference: {0:.2f} %".format(diff[i]), "\t Cash: ", moneyAmount[i])
                outputToCsv([markets[i], askExchange[i], lowestAsk[i], bidExchange[i], highestBid[i], diff[i], moneyAmount[i]])
            else: 
                print(markets[i], "  No profitable pairs")
                outputToCsv([markets[i], '-', '-', '-', '-', '-', '-'])
    else:
        if markets[specifiedIndex] != "BTC-LTC":
            if taxesOn: moneyAmount[specifiedIndex] = decreaseByFee(askExchange[specifiedIndex], moneyAmount[specifiedIndex])
            currencyAmount = moneyAmount[specifiedIndex]/lowestAsk[specifiedIndex]
            if taxesOn: currencyAmount = decreaseByFee(bidExchange[specifiedIndex], currencyAmount)
            moneyAmount[specifiedIndex] = currencyAmount*highestBid[specifiedIndex]
        else:
            moneyAmount[specifiedIndex] = moneyAmount[specifiedIndex]/(exchanges_data[1][0][1].item())
            if taxesOn: moneyAmount[specifiedIndex] = decreaseByFee(askExchange[specifiedIndex], moneyAmount[specifiedIndex])
            currencyAmount = moneyAmount[specifiedIndex]/lowestAsk[specifiedIndex]
            if taxesOn: currencyAmount = decreaseByFee(bidExchange[specifiedIndex], currencyAmount)
            moneyAmount[specifiedIndex] = currencyAmount*highestBid[specifiedIndex]*(exchanges_data[1][0][0].item())
        print(markets[specifiedIndex],"  Buy: ", askExchange[specifiedIndex], " - ", lowestAsk[specifiedIndex], "\tSell: ", bidExchange[specifiedIndex], " - ", highestBid[specifiedIndex],"\tDifference: {0:.2f} %".format(diff[specifiedIndex]), "\t Cash: ", moneyAmount[specifiedIndex])
        outputToCsv([markets[specifiedIndex], askExchange[specifiedIndex], lowestAsk[specifiedIndex], bidExchange[specifiedIndex], highestBid[specifiedIndex], diff[specifiedIndex], moneyAmount[specifiedIndex]])
        return (markets[specifiedIndex], askExchange[specifiedIndex], lowestAsk[specifiedIndex], bidExchange[specifiedIndex], highestBid[specifiedIndex], diff[specifiedIndex], moneyAmount[specifiedIndex])

    record_iter = moneyAmount.index(max(moneyAmount))
    return (markets[record_iter], askExchange[record_iter], lowestAsk[record_iter], bidExchange[record_iter], highestBid[record_iter], diff[record_iter], moneyAmount[record_iter])


def outputToCsv(output):
    f = open('C:/Users/ashig/Documents/Python Scripts/MSiD/profitOutput.csv', 'a+', newline='')
    with f:
        writer = csv.writer(f)
        writer.writerow(output)
    f.close()


def learnFromFile():
    markets_average = [0 for i in range(4)]
    f =  open('C:/Users/ashig/Documents/Python Scripts/MSiD/profitOutput.csv', 'r', newline='')
    counter = 0
    with f:
        reader = csv.reader(f)
        for row in reader:
            counter += 1
            if row[-2] != '-': markets_average[counter%4] = row[-2]
    counter /= 4
    markets_average = [float(market) / counter for market in markets_average] 
    return markets_average.index(max(markets_average))


def currencyMonitor(markets):
    investedSum = 1000
    learntIndex = learnFromFile()
    while True:
        output = printDataBittrex(markets)
        output += printDataBinance(markets)
        output += printDataBitfinex(markets)
        output += printDataBitBay(markets)
        print(output)
        trade = searchProfit(markets, investedSum, False, specifiedIndex = learntIndex)
        if trade[-1] > investedSum: investedSum = trade[-1]
        print("Money sum = ", trade[-1])
        print("\n\n")
        time.sleep(5)
        cls()


def main():
    currencyMonitor(markets)


if __name__ == "__main__":
    main()