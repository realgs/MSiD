from typing import Set

import requests
import csv

MAIN_CURRENCY = "USD"
MARKETS = ['Bittrex', 'Bitbay', 'Bitstamp']

def change_main_currency(new_currency):
    MAIN_CURRENCY = new_currency

def add_resources_to_wallet(currency, value):
    pass

def get_resource_value(currency, value):
    if currency == MAIN_CURRENCY:
        return value
    else:
        order_book = get_orderbook("Bittrex", MAIN_CURRENCY, currency)
        print(order_book)
        ofety_buy = order_book["buy"]
        wartosc = 0
        for i in range(len(ofety_buy)):
            if ofety_buy[i]["qty"]>=value:
                wartosc += value * ofety_buy[i]["price"]
                break
            else:
                wartosc += ofety_buy[i]["qty"] * ofety_buy[i]["price"]
                value -= ofety_buy[i]["qty"]
        if value <= 0:
            print("Brak mozliwosci zamiany " + str(currency) + " na " + str(MAIN_CURRENCY) + " na gieldzie " + str(order_book["name"]))
        print(wartosc)



def get_wallet_value():
    wallet_value = 0
    with open('wallet.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            print(int(row["value"]))
            wallet_value = get_resource_value(row["currency"],int(row["value"]))


def get_orderbook(market_name, market_currency, base_currency):
    if market_name=="Bittrex":
        market_currency = market_currency.upper()
        base_currency = base_currency.upper()
        orderbook = requests.get("https://api.bittrex.com/api/v1.1/public/getorderbook?market=" + market_currency + "-"
                                 + base_currency + "&type=both")
        orderbook_json = orderbook.json()
        if orderbook_json["success"]:
            buy_offer = orderbook_json["result"]["buy"]
            buy = []
            for i in range(len(buy_offer)):
                buy_offerta = {}
                buy_offerta["qty"] = buy_offer[i]["Quantity"]
                buy_offerta["price"] = buy_offer[i]["Rate"]
                buy.append(buy_offerta)

            sell_offer = orderbook_json["result"]["sell"]
            sell = []

            for i in range(len(sell_offer)):
                sell_offerta = {}
                sell_offerta["qty"] = sell_offer[i]["Quantity"]
                sell_offerta["price"] = sell_offer[i]["Rate"]
                sell.append(sell_offerta)

            result = {"name": "bittrex", "buy": buy, "sell": sell}
            return result
        else:
            raise Exception
    elif market_name=="Bitbay":
        market_currency = market_currency.upper()
        base_currency = base_currency.upper()
        orderbook = requests.get("https://bitbay.net/API/Public/" + market_currency + base_currency
                                 + "/orderbook.json")
        orderbook_json = orderbook.json()
        buy = orderbook_json["bids"][0]
        sell = orderbook_json["asks"][0]
        result = ["bitbay", float(buy[1]), float(buy[0]), float(sell[1]), float(sell[0])]
        return result
    elif market_name=="Bitstamp":
        market_currency = market_currency.lower()
        base_currency = base_currency.lower()
        orderbook = requests.get("https://www.bitstamp.net/api/v2/order_book/" + market_currency + base_currency
                                 + "/")
        orderbook_json = orderbook.json()
        buy = orderbook_json["bids"][0]
        sell = orderbook_json["asks"][0]
        result = ["bitstamp", float(buy[1]), float(buy[0]), float(sell[1]), float(sell[0])]
        return result


def main():
    change_main_currency("USD")
    get_wallet_value()


if __name__ == '__main__':
    main()