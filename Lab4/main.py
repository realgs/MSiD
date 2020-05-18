from fetcher import fetchPrices, MarketInfo
from comparator import findLowHighAll, canBeProfitable, calculateTrade
import time

markets = ["USD-BTC", "USD-ETH", "USD-LTC", "USD-XRP"]

def main():
    budget = 1000
    startTime = time.strftime("%x %X", time.gmtime())
    print(f"Starting with budget {budget}$ at {startTime}.")
    while(True):
        for m in markets:
            results = fetchPrices(m)
            results = findLowHighAll(results)
            for r in results:
                for toComp in results:
                    if toComp == r:
                        continue
                    if canBeProfitable(r, toComp):
                        result = calculateTrade(r, toComp, budget)
                        amount = result[0]
                        profit = result[1]
                        currency = r.currency.split("-")
                        print(f"At {r.market:8} you can buy {amount:8.5f} {currency[1]} at rate {r.buyForLowest[1]:8.5f} {currency[0]} and sell at {toComp.market:8} at rate {toComp.sellForHighest[1]:8.5f} {currency[0]} for {profit:.2f} {currency[0]} {'profit' if profit>0 else 'loss'} (including {amount * r.takerFee *toComp.sellForHighest[1]:.2f} {currency[0]} fee).")
                        if profit > 0:
                            timestamp = time.strftime("%x %X", time.gmtime())
                            print(f"{timestamp}: {profit:.2f}$ profit!")
                            budget+=profit
                            print(f"Budget is now {budget:.2f}$ since {startTime}.")

        time.sleep(8)

if __name__ == "__main__":
    main()