import requests
import re
import time

url = f"https://api.bittrex.com/api/v1.1/public/getticker?market=BTC-LTC"

def getData():
	respond = requests.get(url)
	return respond.json()

def getBidAskPair():
	data = str(getData())
	regex = "'Bid'.*?,"
	match = re.search(regex,data)
	intermed = match.group()
	regex = "\d+\.\d+"
	match = re.search(regex,intermed)
	bid = float(match.group())
	regex = "'Ask'.*?,"
	match = re.search(regex,data)
	intermed = match.group()
	regex = "\d+\.\d+"
	match = re.search(regex,intermed)
	ask = float(match.group())
	return (bid,ask)

def printData(pair):
	print("Bid: " + str(pair[0]) + " Ask: " + str(pair[1]))

def printInfo():
	pair = getBidAskPair()
	printData(pair)

def getPercentDifference(pair):
	return 1 - ((pair[1] - pair[0]) / pair[0])

def loop():
	while True:
		pair = getBidAskPair()
		printData(pair)
		print("Percent difference between buy and sell offer: " 
		+ str(getPercentDifference(pair) * 100) + "%")
		time.sleep(5)

loop()
