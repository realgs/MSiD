import requests
import time
from datetime import datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

##LIST 4

markets = ["bitbay", "bitstamp", "bitfinex", "bittrex"]

# dla uproszczenia przyjąłem wartości takera dla $20K
# taker = {
#     "bitbay":0.0038,
#     "bitstamp":0.0025,
#     "bitfinex":0.002,
#     "bittrex":0.002
# }

taker = {
    "bitbay": 0.0005,
    "bitstamp": 0.001,
    "bitfinex": 0.00075,
    "bittrex": 0.001
}

wallet = {
    "USD": 10000.0,
    "EUR": 8000.0,
    "BTC": 2.5,
    "ETH": 10
}

market_currencies = [("USD", "BTC"), ("EUR", "ETH"), ("BTC", "LTC"), ("BTC", "ETH")]


def get_bitbay_orderbook(market_currency, base_currency):
    trades = requests.get(
        "https://bitbay.net/API/Public/{0}{1}/{2}.json".format(base_currency, market_currency, "orderbook"))
    trades_json = trades.json()
    result = ["bitbay", trades_json['bids'][0][0], trades_json['bids'][0][1], trades_json['asks'][0][0],
              trades_json['asks'][0][1]]
    return result


def get_bitstamp_orderbook(market_currency, base_currency):
    code = base_currency + market_currency
    code = code.lower()
    trades = requests.get(
        "https://www.bitstamp.net/api/v2/order_book/{0}".format(code))
    trades_json = trades.json()
    result = ["bitstamp", float(trades_json['bids'][0][0]), float(trades_json['bids'][0][1]),
              float(trades_json['asks'][0][0]),
              float(trades_json['asks'][0][1])]
    return result


def get_bitfinex_orderbook(market_currency, base_currency):
    code = base_currency + market_currency
    code = code.upper()
    trades = requests.get(
        "https://api-pub.bitfinex.com/v2/book/t{0}/P0?len=1".format(code))
    trades_json = trades.json()
    result = ["bitfinex", trades_json[0][0], trades_json[0][2], trades_json[1][0], -1 * trades_json[1][2]]
    return result


def get_bittrex_orderbook(makret_currency, base_currency):
    notice = makret_currency + "-" + base_currency
    notice = notice.upper()
    orderbook = requests.get(
        "https://api.bittrex.com/api/v1.1/public/getorderbook?market={0}&type=both".format(notice))
    orderbook_json = orderbook.json()

    buy = orderbook_json["result"]["buy"]
    sell = orderbook_json["result"]["sell"]
    result = ["bittrex", buy[0]['Rate'], buy[0]['Quantity'], sell[0]['Rate'], sell[0]['Quantity']]
    return result


def arbitrage_checker():
    while True:
        for currencies in market_currencies:
            check_arbitrage(currencies[0], currencies[1])
        time.sleep(10)


def check_arbitrage(market_currency, base_currency):
    bitbay_data = get_bitbay_orderbook(market_currency, base_currency)
    bitstamp_data = get_bitstamp_orderbook(market_currency, base_currency)
    bitfinex_data = get_bitfinex_orderbook(market_currency, base_currency)
    bittrex_data = get_bittrex_orderbook(market_currency, base_currency)

    full_data = [bitbay_data, bitstamp_data, bitfinex_data, bittrex_data]
    for data in full_data:
        best_sell_data = None
        best_sell_value = 0
        for data_sell in full_data:
            if data != data_sell:
                # print(data_sell)
                if (data_sell[1] > best_sell_value):
                    best_sell_data = data_sell
                    best_sell_value = data_sell[1]
        # print("BEST")
        # print(best_sell_data)
        check_buy_sell_profit(data, best_sell_data, market_currency, base_currency)


def check_buy_sell_profit(market_data_buy, market_data_sell, market_currency, base_currency):
    if market_data_buy[3] < market_data_sell[1]:
        amount = market_data_buy[4] if market_data_buy[4] <= market_data_sell[2] else market_data_sell[2]
        # profit = (amount * (market_data_sell[1] * (1 - taker[market_data_sell[0]]) - market_data_buy[3] * (
        #         1 + taker[market_data_buy[0]])))
        profit = (amount * (market_data_sell[1] - market_data_buy[3]))
        if (profit > 0):
            to_invest = amount * market_data_buy[3]
            if (to_invest > wallet[market_currency]):
                amount = (wallet[market_currency] / to_invest) * amount
            print(
                "Na giełdzie {0} można kupić {1} {2} za {3} po kursie {4} i sprzedać na giełdzie {5} po kursie {6}, zyskując {7} {8}".format(
                    market_data_buy[0], amount, base_currency, market_currency, market_data_buy[3],
                    market_data_sell[0], market_data_sell[1],
                    profit, market_currency))
            wallet[market_currency] += profit
            print_wallet()
    # else:
    # print("NO PROFIT")


def print_wallet():
    print("MY WALLET: " + str(wallet))


# Trying ex. 4 for bittrex
bittrex_buy_data = {
    market_currencies[0]: [],
    market_currencies[1]: [],
    market_currencies[2]: [],
    market_currencies[3]: []
}
bittrex_sell_data = {
    market_currencies[0]: [],
    market_currencies[1]: [],
    market_currencies[2]: [],
    market_currencies[3]: []
}


def analizer():
    while True:
        for currencies in market_currencies:
            analyze_market(currencies[0], currencies[1], currencies)
        plot_maker()
        time.sleep(5)


def analyze_market(market_currency, base_currency, currencies):
    bittrex_data = get_bittrex_orderbook(market_currency, base_currency)
    handle_buy_data(bittrex_data,currencies)
    handle_sell_data(bittrex_data,currencies)
    print(bittrex_buy_data)
    print(bittrex_sell_data)



def handle_buy_data(buy_data,currencies):
    print(buy_data)
    bittrex_buy_data[currencies].append(buy_data[3])
    print("B " + buy_data[0])
    print("AVERAGE")
    average = sum(bittrex_buy_data[currencies]) / len(bittrex_buy_data[currencies])
    print(average)
    print("MEAN SQUARED ERROR")
    print(calc_mean_squared_error(average, bittrex_buy_data[currencies]))


def handle_sell_data(sell_data,currencies):
    bittrex_sell_data[currencies].append(sell_data[1])
    print("S " + sell_data[0])
    average = sum(bittrex_sell_data[currencies]) / len(bittrex_sell_data[currencies])
    print(average)
    print("MEAN SQUARED ERROR")
    print(calc_mean_squared_error(average, bittrex_sell_data[currencies]))


def calc_mean_squared_error(average, data_to_calc):
    size = len(data_to_calc)
    sum = 0
    for data in data_to_calc:
        sum += (data - average) ** 2
    return sum / size


def plot_maker():
    for currencies in market_currencies:
        buy_data = bittrex_buy_data[currencies]
        sell_data = bittrex_sell_data[currencies]
        plt.title(currencies)
        plt.ylabel("Price")
        plt.xlabel("Iteration")
        buy_line = plt.plot([buy_data[i] for i in range(len(buy_data))], label="BUY")
        sell_line = plt.plot([sell_data[i] for i in range(len(sell_data))], label="SELL")
        plt.show()


##LIST 3

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
    arbitrage_checker()
    # analizer()


if __name__ == "__main__":
    main()
