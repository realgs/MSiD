from fetcher import fetchPrices, MarketInfo
from comparator import findLowHigh
import time

markets = ["USD-BSV", "USD-BTC", "USD-LTC", "USD-ETH"]

def main():
    while(True):
        results = fetchPrices(markets)
        timestamp = time.strftime("%x %X", time.gmtime())
        for r in results:
            for toComp in results:
                if toComp == r:
                    continue
                print(f"Comparing {r.currency} between {r.name} and {toComp.name}")
                

        time.sleep(5)

if __name__ == "__main__":
    main()