from fetcher import fetchMarkets, fetchPrices
from random import randint
import time

maxRandomMarkets = 5

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
    markets = pickRandomNames(allNames)
    while(True):
        print("-"*68)
        print("|   Name   |    Bid    |    Ask    |    Dif    |    Timestamp    |")
        print("-"*68)
        timestamp = time.strftime("%x %X", time.gmtime())
        results = fetchPrices(markets)
        for r in results:
            name = r[0]
            bid = r[1]
            ask = r[2]
            diff = ((ask - bid)/ask) * 100
            print(f"{name:10}  {bid:.8f}   {ask:.8f}   {diff:.4f}%   {timestamp}")
        time.sleep(5)

if __name__ == "__main__":
    main()