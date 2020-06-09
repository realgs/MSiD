import requests
import time
from datetime import datetime


def check_market_availability(market_currency, base_currency):
    markets = requests.get("https://api.bittrex.com/api/v1.1/public/getmarkets")
    markets_json = markets.json()
    market_info = [(result["MarketCurrency"].upper(), result["MarketCurrencyLong"].upper(),
                    result["BaseCurrency"].upper(), result["BaseCurrencyLong"].upper()) for result in
                   markets_json["result"]]
    market_currency = market_currency.upper()
    base_currency = base_currency.upper()
    for market in market_info:
        if (market_currency == market[0] or market_currency == market[1]) and (
                base_currency == market[2] or base_currency == market[3]):
            return True, market
    return False, None


def get_offers(market_currency, base_currency, amount_of_orders):
    exists, market = check_market_availability(market_currency, base_currency)
    data_time = datetime.now()
    if exists:
        notice = market[2] + "-" + market[0]
        orderbook = requests.get(
            "https://api.bittrex.com/api/v1.1/public/getorderbook?market={0}&type=both".format(notice))
        orderbook_json = orderbook.json()
        print("{0} market top {1} offers: ({2})".format(notice, amount_of_orders, data_time.strftime("%H:%M:%S")))
        print("BUY: ")
        print("{:>12s}   {:>10s}".format("QUANTITY", "RATE"))
        for i in range(0, amount_of_orders):
            buy_quantity = orderbook_json["result"]["buy"][i]["Quantity"]
            buy_rate = orderbook_json["result"]["buy"][i]["Rate"]
            print("{:12.8f} : {:.8f}".format(buy_quantity, buy_rate))

        print("SELL: ")
        print("{:>12s}   {:>10s}".format("QUANTITY", "RATE"))
        for i in range(0, amount_of_orders):
            sell_quantity = orderbook_json["result"]["sell"][i]["Quantity"]
            sell_rate = orderbook_json["result"]["sell"][i]["Rate"]
            print("{:12.8f} : {:.8f}".format(sell_quantity, sell_rate))
        buy_sell_rates = [(orderbook_json["result"]["buy"][i]["Rate"], orderbook_json["result"]["sell"][i]["Rate"]) for
                          i in range(0, amount_of_orders)]
        return buy_sell_rates
    else:
        print("THIS MARKET DOESN'T EXIST")


def monitor_top_offer(market_currency, base_currency, amount_of_orders, interval):
    exists, market = check_market_availability(market_currency, base_currency)
    if exists:
        if interval >= 0.5:
            while True:
                start_time = time.time()
                buy_sell_rates = get_offers(market_currency, base_currency, amount_of_orders)
                print("BUY/SELL DIFFERENCES: ")
                for rate in buy_sell_rates:
                    buy_price, sell_price = rate
                    difference = 1 - (sell_price - buy_price) / buy_price
                    print("{:.7f}".format(difference))
                print()
                end_time = time.time()
                time.sleep(interval - (end_time - start_time))
        else:
            print("THE REFRESH RATE IS TOO SMALL")
    else:
        print("THIS MARKET DOESN'T EXIST")


def main():
    get_offers("LTC", "BTC", 5)
    get_offers("Bitcoin", "USD", 3)
    monitor_top_offer("LTC", "BTC", 5, 5.0)


if __name__ == "__main__":
    main()
