from fetcher import fetchMarkets, fetchPrices
from random import randint
import time

maxRandomMarkets = 5
customMarkets = ["BTC-LTC", "USD-BSV", "USD-BTC", "USD-LTC", "USD-ETH"]

def pickRandomNames(allNames):
    namesTemp = allNames.copy()
    output = []
    for _ in range(0, maxRandomMarkets):
        if len(namesTemp) == 0:
            break
        index = randint(0, len(namesTemp))
        name = namesTemp[index]
        output.append(name)
        namesTemp.remove(name)
    return output

def main():
    allNames = fetchMarkets()
    markets = None
    if input("Load custom markets? (Y/N)") == "N":
        markets = pickRandomNames(allNames)
    else:
        markets = customMarkets
    while(True):
        results = fetchPrices(markets)
        print("-"*81)
        print("|   Name   |      Bid      |      Ask      |      Dif      |      Timestamp     |")
        print("-"*81)
        timestamp = time.strftime("%x %X", time.gmtime())
        for r in results:
            name = r[0]
            bid = r[1]
            ask = r[2]
            diff = ((ask - bid)/ask) * 100
            print(f"  {name:10} {bid:14.8f} {ask:14.8f} {diff:14.8f}%     {timestamp}")
        time.sleep(5)

if __name__ == "__main__":
    main()