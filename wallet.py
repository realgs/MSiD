import requests
import json


class Wallet:

    def isAPIAgreedWithWallet(self):
        for coin in self.coinsInWallet:
            if coin not in self.supportedCurrencies:
                print("API can not handle {}".format(coin))
                return False
        return True

    def getCurrencies(self):
        url = "https://api.bitbay.net/rest/trading/stats"
        response = requests.request("GET", url)
        pairsOfCurrencies = response.json()['items']
        for pair in pairsOfCurrencies:
            self.supportedCurrencies.update(pair.split('-'))

    def __init__(self, baseCurrency):
        self.supportedCurrencies = {'BTC'}
        self.coinsInWallet = {}
        self.getCurrencies()
        self.baseCurrency = baseCurrency
        with open("walletData.json", "r") as readFile:
            self.coinsInWallet = json.load(readFile)
        if not self.isAPIAgreedWithWallet():
            print("Błąd")

    def estimateWalletValue(self):
        value = 0.0
        for coinInWallet in self.coinsInWallet:
            if coinInWallet == self.baseCurrency:
                value = value + self.coinsInWallet[coinInWallet]
            else:
                url = "https://api.bitbay.net/rest/trading/orderbook/{}-{}".format(
                    coinInWallet,self.baseCurrency)
                response = requests.request("GET", url)
                if response.json()['status'] == 'Fail':
                    url = "https://api.bitbay.net/rest/trading/orderbook/{}-{}".format(
                        self.baseCurrency, coinInWallet)
                    response = requests.request("GET", url)
                    if response.json()['status'] == 'Fail':
                        print("Nie potrafię przekonwertować {} do {}".format(
                            coinInWallet, self.baseCurrency))
                    else:
                        value = value + self.coinsInWallet[coinInWallet]*(1/float(response.json()['sell'][0]['ra']))
                else:
                    value = value + self.coinsInWallet[coinInWallet]*float(response.json()['sell'][0]['ra'])
        return value

    def save(self):
        with open("walletData.json", "w") as writeFile:
            json.dump(self.coinsInWallet, writeFile, indent=4)

    def addToWallet(self, currency, amount):
        currency = currency.upper()
        print(type(amount))
        if currency not in self.supportedCurrencies:
            print("Currency is not supported, sorry :C")
            return
        if currency in self.coinsInWallet:
            self.coinsInWallet[currency] = self.coinsInWallet[currency]+amount
        else:
            self.coinsInWallet[currency] = amount
        self.save()

    def removeFromWallet(self, currency, amount):
        currency = currency.upper()
        if currency not in self.supportedCurrencies:
            print("Currency is not supported, sorry :C")
            return
        if currency not in self.coinsInWallet:
            return
        self.coinsInWallet[currency] = self.coinsInWallet[currency] - amount
        if self.coinsInWallet[currency] <= 0:
            del self.coinsInWallet[currency]
        self.save()

    def showWallet(self):
        print("Stan porfela: ")
        for coin, amount in self.coinsInWallet.items():
            print("{} {}".format(amount,coin))
        print()
        if self.baseCurrency == "BTC":
            print("Portfel ma wartość = {:.8f} {}".format(self.estimateWalletValue(), self.baseCurrency))
        else:
            print("Portfel ma wartość = {:.2f} {}".format(self.estimateWalletValue(), self.baseCurrency))
