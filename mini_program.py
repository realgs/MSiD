from json.decoder import JSONDecodeError

import requests
import csv

MAIN_CURRENCY = "USD"
MARKETS = ['Bittrex', 'Bitbay', 'Bitstamp']


def change_main_currency(new_currency):
    MAIN_CURRENCY = new_currency


def change_resources_in_wallet(type, currency, value=0):
    currency = currency.upper()
    if check_currency_already_in_wallet(currency):
        with open('wallet.csv', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile.readlines())
        with open('wallet.csv', mode="w", encoding='utf-8', newline='') as newcsvfile:
            newcsvwriter = csv.writer(newcsvfile)
            for row in csvreader:
                if row[0] == currency:
                    if type == "add":
                        newcsvwriter.writerow([row[0], int(row[1]) + value])
                    elif type == "change":
                        newcsvwriter.writerow([row[0], value])
                    elif type == "remove":
                        pass
                    else:
                        raise Exception
                else:
                    newcsvwriter.writerow(row)
    else:
        with open('wallet.csv', mode='a', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow('')
            csvwriter.writerow([currency,value])


def check_currency_already_in_wallet(currency):
    with open('wallet.csv', mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if row["currency"] == currency:
                return True
    return False


def get_resource_value(currency, value):
    if currency == MAIN_CURRENCY:
        print("Waluta nie została wymienona z uwagi na identyczność skrótu. Wartość 200" + currency)
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
                    print(f"Waluta została wymieniona na giełdzie {MARKETS[number_of_markets]} i uzyskaliśmy {wartosc:>.8f} {MAIN_CURRENCY}")
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
    with open('wallet.csv', mode='r', encoding='utf-8', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            print(f"Wymiana {row['value']} {row['currency']}")
            wallet_value = get_resource_value(row["currency"],int(row["value"]))
            print()
    return wallet_value


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


def available_currency_pairs(market):
    if market == "Bittrex":
        currencies = requests.get("https://api.bittrex.com/api/v1.1/public/getmarketsummaries")
        try:
            currencies_json = currencies.json()
        except JSONDecodeError:
            raise Exception
        for i in range(len(currencies_json["result"])):
            if i % 10 == 0 and i != 0:
                print(currencies_json["result"][i]["MarketName"])
            elif i == len(currencies_json["result"]) - 1:
                print(currencies_json["result"][i]["MarketName"])
            else:
                print(currencies_json["result"][i]["MarketName"], end=", ")
    elif market == "Bitbay":
        print("Brak możliwości sprawdzenia dostępnych par walut")
    elif market == "Bitstamp":
        currencies = requests.get("https://www.bitstamp.net/api/v2/trading-pairs-info/")
        try:
            currencies_json = currencies.json()
        except JSONDecodeError:
            raise Exception
        for i in range(len(currencies_json)):
            if i % 10 == 0 and i != 0:
                print(currencies_json[i]["name"])
            elif i == len(currencies_json) - 1:
                print(currencies_json[i]["name"])
            else:
                print(currencies_json[i]["name"], end=", ")



def main():
    #change_main_currency("USD")
    #change_resources_in_wallet("add", "ETH", 12)
    #change_resources_in_wallet("remove", "ASE")
    #change_resources_in_wallet("change", "USD", 400)
    #get_wallet_value()
    dostepne_pary_walut("Bitstamp")


if __name__ == '__main__':
    main()