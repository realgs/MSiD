from json.decoder import JSONDecodeError
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
        number_of_markets = 0
        waluta_wymieniona = False
        while not (not (number_of_markets < len(MARKETS)) or (waluta_wymieniona)):
            try:
                order_book = get_orderbook(MARKETS[number_of_markets], MAIN_CURRENCY, currency)
                ofety_buy = order_book["buy"]
                wartosc = 0
                for i in range(len(ofety_buy)):
                    if ofety_buy[i]["qty"] >= value:
                        wartosc += value * ofety_buy[i]["price"]
                        value = 0
                        break
                    else:
                        wartosc += ofety_buy[i]["qty"] * ofety_buy[i]["price"]
                        value -= ofety_buy[i]["qty"]
                if value <= 0:
                    print("Waluta została wymieniona na giełdzie " + str(MARKETS[number_of_markets]) + " i uzyskaliśmy "
                          + str(wartosc) + str(MAIN_CURRENCY))
                    waluta_wymieniona = True
                else:
                    print("Brak możliwości zamiany " + str(currency) + " na " + str(
                        MAIN_CURRENCY) + " na giełdzie " + str(order_book["name"]))
            except Exception:
                print("Brak możliwości sprawdzenia cen na giełdzie " + str(MARKETS[number_of_markets]) + " dla nasepującej pary: " +
                      MAIN_CURRENCY + "-" + currency)
            number_of_markets += 1


def get_wallet_value():
    wallet_value = 0
    with open('wallet.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            print("Wymiana " + str(row["value"]) + " " + str(row["currency"]))
            wallet_value = get_resource_value(row["currency"],int(row["value"]))
            print()


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
        orderbook = requests.get("https://bitbay.net/API/Public/" + base_currency + market_currency
                                 + "/orderbook.json")
        orderbook_json = orderbook.json()
        if not "code" in orderbook_json.keys():
            buy_offer = orderbook_json["bids"]
            buy = []
            for i in range(len(buy_offer)):
                buy_offerta = {}
                buy_offerta["qty"] = buy_offer[i][1]
                buy_offerta["price"] = buy_offer[i][0]
                buy.append(buy_offerta)

            sell_offer = orderbook_json["asks"]
            sell = []

            for i in range(len(sell_offer)):
                sell_offerta = {}
                sell_offerta["qty"] = sell_offer[i][1]
                sell_offerta["price"] = sell_offer[i][0]
                sell.append(sell_offerta)

            result = {"name": "bitbay", "buy": buy, "sell": sell}
            print(result)
            return result
        else:
            raise Exception
    elif market_name=="Bitstamp":
        market_currency = market_currency.lower()
        base_currency = base_currency.lower()
        orderbook = requests.get("https://www.bitstamp.net/api/v2/order_book/" + base_currency + market_currency
                                 + "/")
        try:
            orderbook_json = orderbook.json()
        except JSONDecodeError:
            raise Exception

        buy_offer = orderbook_json["bids"]
        buy = []
        for i in range(len(buy_offer)):
            buy_offerta = {}
            buy_offerta["qty"] = buy_offer[i][1]
            buy_offerta["price"] = buy_offer[i][0]
            buy.append(buy_offerta)

        sell_offer = orderbook_json["asks"]
        sell = []

        for i in range(len(sell_offer)):
            sell_offerta = {}
            sell_offerta["qty"] = sell_offer[i][1]
            sell_offerta["price"] = sell_offer[i][0]
            sell.append(sell_offerta)

        result = {"name": "bitstamp", "buy": buy, "sell": sell}
        print(result)
        return result


def main():
    change_main_currency("USD")
    get_wallet_value()


if __name__ == '__main__':
    main()