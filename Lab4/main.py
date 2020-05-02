from fetcher import fetchPrices, MarketInfo
from comparator import findLowHighAll, canBeProfitable, calculateTrade
import time

markets = ["USD-BTC", "USD-ETH", "USD-LTC", "USD-XRP"]

def main():
    while(True):
        for m in markets:
            results = fetchPrices(m)
            results = findLowHighAll(results)
            for r in results:
                for toComp in results:
                    if toComp == r:
                        continue
                    isProfitable = canBeProfitable(r, toComp)
                    if isProfitable:
                        profit = calculateTrade(r, toComp)
                        if profit > 0:
                            timestamp = time.strftime("%x %X", time.gmtime())
                            print(f"{timestamp}: {profit:.5f}$ profit!")


        time.sleep(10)

if __name__ == "__main__":
    main()