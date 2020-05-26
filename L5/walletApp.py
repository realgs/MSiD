import requests
import json
import time 
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime
import os
import sys
import matplotlib.pyplot as plt

class Currency:
    currencyName = ""
    amount = ""

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def __str__(self):
        return " Name: " + str(self.name) + " | "+ str(self.amount) + " amount"

    def __repr__(self):
        return " Name: " + str(self.name) + " | "+ str(self.amount) + " amount"

class Wallet: 
    baseCurrency = ""
    resources = []
    walletPath = ""

    def __init__(self, baseCurrency):
        self.baseCurrency = baseCurrency


    def addResource(self, currency, amount):
        resource = Currency(currency, amount)

        if any(res.name == currency for res in self.resources):
            for resourceInList in self.resources:
                if resourceInList.name == resource.name:
                    resourceInList.amount += amount
        else:
            self.resources.append(resource)
        appendToJson(self)

    def substractResource(self, currency, amount):
        if any(res.name == currency for res in self.resources):
            for resourceInList in self.resources:
                if resourceInList.name == currency:
                    resourceInList.amount -= amount
                    if resourceInList.amount < 0: resourceInList.amount = 0
        else: print("There is nothing to substract from!")
        appendToJson(self)
    
    def removeResource(self, currency):
        indexToRm = ""
        for index in range(len(self.resources)):
            if self.resources[index].name == currency:
                indexToRm = index

        if indexToRm != "": del self.resources[indexToRm]  
        else: print("There is nothing to remove")
        appendToJson(self)

    def loadFromFile(self):
        if os.stat(self.walletPath).st_size == 0:
            print("File is empty")
            return

        with open(self.walletPath, "r+") as outfile:
            json_data = json.load(outfile)
            lengthOfReadings = len(json_data['walletReadings'])

            print(json_data['walletReadings'][lengthOfReadings - 1])
            for key in json_data['walletReadings'][lengthOfReadings - 1].keys():
                currencyName = str(key)
                amount = json_data['walletReadings'][lengthOfReadings - 1][key]
                self.resources.append(Currency(currencyName, amount))
    

def calculateWalletValue(wallet):
    walletValue = 0.0
    for resource in wallet.resources:
        walletValue += calculateValueOfResource(wallet.baseCurrency, resource)
    print("Accumulated value: " + str(walletValue) + " " + str(wallet.baseCurrency))


def calculateValueOfResource(baseCurrency, resource):
    if baseCurrency == resource.name:
        print(baseCurrency + "-" + str(resource.name) + ", cannot be performed")
        return 0

    response = requests.get("https://api.bittrex.com/api/v1.1/public/getorderbook?market={0}-{1}&type=both".format(baseCurrency, resource.name))
    json_data = response.json()
    
    buyers = sorted(json_data['result']['buy'], key=lambda k: k['Rate'], reverse=True)

    amountOfCurrency = resource.amount
    currencies = []
    value = 0
    for buyer in buyers:
        amountOfCurrency -= buyer['Quantity']
        if amountOfCurrency > 0: 
            value += buyer['Quantity'] * buyer['Rate']
        else: amountOfCurrency += buyer['Quantity']

    print(str(resource.name).upper() + " value: " + str(value))    
    return value


def showChartsOfReadings(wallet, currencyName):
    amountOfCurrency = []

    with open(wallet.walletPath, "r") as readfile:
        data = json.load(readfile)
        for readings in data['walletReadings']:
            if currencyName in readings:
                amountOfCurrency.append(readings[currencyName])
            else: amountOfCurrency.append(0)

    fig = plt.figure()
    fig.suptitle("Chart of " + str(currencyName) + " amount")

    plt.plot(amountOfCurrency, label=str(currencyName))

    plt.xlabel('Readings')
    plt.ylabel('Amount')

    plt.legend()
    plt.show()


def checkIsCurrencySupported(name):
    supportedCurrencies = []
    response = requests.get("https://api.bittrex.com/api/v1.1/public/getcurrencies")
    json_data = response.json()

    for currency in json_data["result"]:
        supportedCurrencies.append(currency["Currency"])

    if name in supportedCurrencies:
        return True
    else: return False

def choosingFile(wallet):
    response = input("Enter (1) to use default wallet, if you want to load your own click (2): ")
    if response == "1":
        wallet.walletPath = "wallet.json"
    elif response == "2":
        Tk().withdraw()
        filename = askopenfilename()
        wallet.walletPath = filename
    else: 
        print("Unknown operation, please try one more time.")
        choosingFile(wallet)

def createWalletJson(wallet):
    data = {}

    data['walletReadings'] = []
    data['walletReadings'].append({
        currency.name: currency.amount for currency in wallet.resources    
    })
        
    with open(wallet.walletPath, 'w') as outfile:
        json.dump(data, outfile)

def appendToJson(wallet):
    if os.stat(wallet.walletPath).st_size == 0:
        createWalletJson(wallet)
    else:
        with open(wallet.walletPath, "r+") as outfile:
            data = json.load(outfile)
            data['walletReadings'].append({
                currency.name: currency.amount for currency in wallet.resources    
            })

            outfile.seek(0)
            json.dump(data, outfile)



def main():
    baseCurrency = input("Enter base currency (USD or BTC): ")
    if baseCurrency in ['USD', 'BTC']:
        wallet = Wallet(baseCurrency)
    else: 
        print("Please enter valid one.")
        main()
    
    choosingFile(wallet)
    wallet.loadFromFile()

    while True:
        print(""" 
Please select one from following:
    1 -> Show me value of my wallet
    2 -> Add amount of currency to my wallet (can be new one)
    3 -> Substract amount of currency from my wallet
    4 -> Remove currency from my wallet
    5 -> Show me history chart of one of my currencies amounts
    6 -> Show me my current amounts of currencies
    E -> (E)xit

    Waiting for your response...  
         """)
        
        response = input()

        if response == "E":
            appendToJson(wallet)
            sys.exit()
        elif response == "1":
            calculateWalletValue(wallet)
        elif response ==  "2":
            currencyName = input("Name of currency to add amount (eg. 'BTC'): ")
            if checkIsCurrencySupported(currencyName): 
                currencyAmount = float(input("Amount of currency: "))
                if currencyAmount <= 0:
                    print("If you want to substract choose (4)")
                else: 
                    wallet.addResource(currencyName, currencyAmount)
                    print("Succesful!")
            else: print("This currency is not supported!")
        elif response ==  "3":
            currencyName = input("Name of currency to substract from (eg. 'BTC'): ")
            currencyAmount = float(input("Substract amount: "))
            if currencyAmount <= 0:
                print("If you want to substract choose (4)")
            else: 
                wallet.substractResource(currencyName, currencyAmount)
                print("Succesful!")
        elif response ==  "4":
            currencyName = input("Name of currency to remove (eg. 'BTC'): ")
            wallet.removeResource(currencyName)

        elif response ==  "5":
            currencyName = input("Name of currency to make chart on: ")
            showChartsOfReadings(wallet, currencyName)
        elif response ==  "6":
            for currency in wallet.resources:
                print(currency)
        else: print("Oh I think your finger slipped, try one more time!")


main()