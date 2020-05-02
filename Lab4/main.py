from fetcher import fetchPrices, MarketInfo
from comparator import findLowHighAll, canBeProfitable, calculateTrade
import time

#markets = ["USD-BSV", "USD-BTC", "USD-LTC", "USD-ETH"]
markets = ["USD-BTC"]

def main():
    while(True):
        results = fetchPrices(markets[0])
        timestamp = time.strftime("%x %X", time.gmtime())
        results = findLowHighAll(results)
        #print(f"{timestamp} - Comparing results...")
        for r in results:
            for toComp in results:
                if toComp == r:
                    continue
                #print(f"Comparing {r.currency} between {r.market} and {toComp.market}")
                isProfitable = canBeProfitable(r, toComp)
                #print(f"Can profit: {isProfitable}")
                if isProfitable:
                    calculateTrade(r, toComp)

        time.sleep(5)

if __name__ == "__main__":
    main()