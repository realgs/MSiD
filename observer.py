import sys
import time
from datetime import datetime

import requests

market_currencies = [("LTC", "BTC"), ("ETH", "BTC"), ("BTC", "USD"), ("XRP", "BTC")]
time_period = 25  # 25 - minimalny czas
bitbay_fee = 0.1  # brak informacji do pobrania w API
bitstamp_fee = 0.1  # brak informacji do pobrania w API


def get_bittrex_orderbook(market_currency, base_currency):
    market_currency = market_currency.upper()
    base_currency = base_currency.upper()
    orderbook = requests.get("https://api.bittrex.com/api/v1.1/public/getorderbook?market=" + market_currency + "-"
                             + base_currency + "&type=both")
    orderbook_json = orderbook.json()
    if orderbook_json["success"]:
        buy = orderbook_json["result"]["buy"][0]
        sell = orderbook_json["result"]["sell"][0]
        result = ["bittrex", float(buy["Quantity"]), float(buy["Rate"]), float(sell["Quantity"]), float(sell["Rate"])]
        return result


def get_bitbay_orderbook(market_currency, base_currency):
    market_currency = market_currency.upper()
    base_currency = base_currency.upper()
    orderbook = requests.get("https://bitbay.net/API/Public/" + market_currency + base_currency
                             + "/orderbook.json")
    orderbook_json = orderbook.json()
    buy = orderbook_json["bids"][0]
    sell = orderbook_json["asks"][0]
    result = ["bitbay", float(buy[1]), float(buy[0]), float(sell[1]), float(sell[0])]
    return result


def get_bitstamp_orderbook(market_currency, base_currency):
    market_currency = market_currency.lower()
    base_currency = base_currency.lower()
    orderbook = requests.get("https://www.bitstamp.net/api/v2/order_book/" + market_currency + base_currency
                             + "/")
    orderbook_json = orderbook.json()
    buy = orderbook_json["bids"][0]
    sell = orderbook_json["asks"][0]
    result = ["bitstamp", float(buy[1]), float(buy[0]), float(sell[1]), float(sell[0])]
    return result


def get_bittrex_fee(currency):
    currency = currency.upper()
    currencies = requests.get("https://api.bittrex.com/api/v1.1/public/getcurrencies")
    currencies_json = currencies.json()
    result = currencies_json["result"]
    fee = 0
    for information in result:
        if information["Currency"] == currency:
            fee = information["TxFee"]
    return fee


def get_transaction_fee(currency, exchange):
    if exchange == "bitbay":
        return bitbay_fee
    elif exchange == "bitstamp":
        return bitstamp_fee
    elif exchange == "bittrex":
        return get_bittrex_fee(currency)


def get_profitable_arbitration_table(currency1, currency2):
    bittrex_orderbook = get_bittrex_orderbook(currency2, currency1)
    bitbay_orderbook = get_bitbay_orderbook(currency1, currency2)
    bitstamp_orderbook = get_bitstamp_orderbook(currency1, currency2)
    all_orderbook = [bittrex_orderbook, bitbay_orderbook, bitstamp_orderbook]
    profitable_arbitration_table = []

    the_cheapest_offer_to_buy = ("Null", 0, sys.float_info.max)
    for market_offer_sell in all_orderbook:
        if market_offer_sell[4] < the_cheapest_offer_to_buy[2]:
            the_cheapest_offer_to_buy = (market_offer_sell[0], market_offer_sell[3], market_offer_sell[4])
    for offer_to_sell in all_orderbook:
        profit = check_profit_from_arbitration(the_cheapest_offer_to_buy, offer_to_sell, currency1, currency2)
        if profit[0] > 0:
            profitable_arbitration_table.append([the_cheapest_offer_to_buy[0], profit[1], the_cheapest_offer_to_buy[2],
                                                 offer_to_sell[0], offer_to_sell[1], offer_to_sell[2], profit[0]])
    return profitable_arbitration_table


def check_profit_from_arbitration(the_cheapest_offer_to_buy, offer_to_sell, waluta1, waluta2):
    if the_cheapest_offer_to_buy[1] < offer_to_sell[1]:
        amount_of_currency = the_cheapest_offer_to_buy[1]
    else:
        amount_of_currency = offer_to_sell[1]
    buy_fee = get_transaction_fee(waluta2, the_cheapest_offer_to_buy[0])
    sell_fee = get_transaction_fee(waluta1, offer_to_sell[0])
    earned_difference = (amount_of_currency*offer_to_sell[2]*(1-buy_fee)) - \
                        (amount_of_currency*the_cheapest_offer_to_buy[2]*(1+sell_fee))
    return earned_difference, amount_of_currency


def explore_stock_exchanges():
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    print(f"Data obliczeń: {current_time}")
    for pair_currencies in market_currencies:
        profitable_arbitration_table = get_profitable_arbitration_table(pair_currencies[0], pair_currencies[1])
        if not profitable_arbitration_table:
            print(f"\t Dla waluty {pair_currencies[0]} oraz {pair_currencies[1]} nie ma możliwości przeprowadzenia "
                  f"arbitrażu z zyskiem.")
        else:
            for result in profitable_arbitration_table:
                print(f"\t Na giełdzie {result[0]} można kupić {result[1]} {pair_currencies[0]} za {pair_currencies[1]}"
                      f" po kursie {result[2]:>.8f} i sprzedać na giełdzie {result[3]} po kursie {result[5]:>.8f},"
                      f" zyskując {result[6]:>.8f}{pair_currencies[1]}.")
    print()


def main():
    while True:
        explore_stock_exchanges()
        time.sleep(time_period)


if __name__ == '__main__':
    main()
