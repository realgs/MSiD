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
        currency_exchanged = False
        while not (not (number_of_markets < len(MARKETS)) or currency_exchanged):
            try:
                order_book = get_orderbook(MARKETS[number_of_markets], MAIN_CURRENCY, currency)
                offers_buy = order_book["buy"]
                resource_value = 0
                for i in range(len(offers_buy)):
                    if offers_buy[i]["qty"] >= value:
                        resource_value += value * offers_buy[i]["price"]
                        value = 0
                        break
                    else:
                        resource_value += offers_buy[i]["qty"] * offers_buy[i]["price"]
                        value -= offers_buy[i]["qty"]
                if value <= 0:
                    print(f"Waluta została wymieniona na giełdzie {MARKETS[number_of_markets]} i uzyskaliśmy {resource_value:>.2f} {MAIN_CURRENCY}")
                    currency_exchanged = True
                else:
                    print(f"Brak możliwości zamiany {currency} na {MAIN_CURRENCY} na giełdzie {order_book['name']}")
            except Exception:
                print(f"Brak możliwości sprawdzenia cen na giełdzie {MARKETS[number_of_markets]} dla nasepującej pary: {MAIN_CURRENCY} - {currency}")
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

def czy_poprawna_nazwa_waluty(currency):
    if len(currency) == 3:
        return True


def run():
    print("Witamy w programie pomgającym ogarnąć Kryptowaluty i Kryptogiełdy :)")
    end = False
    while not end:
        print("Wybierz co chcesz zrobić:\n"
              "1. Zmień walutę przelicznika\n"
              "2. Dodaj walutę do portfela\n"
              "3. Usuń walutę z portfela\n"
              "4. Zmień ilość waluty z portfela\n"
              "5. Przelicz portfel\n"
              "6. Wyświetl dostępne waluty na giełdzie: 'Bitbay','Bittrex','Bitstamp'\n"
              "7. Zakończ program")
        choice = input()
        if choice == "1":
            correct = False
            while not correct:
                print("Podaj skrót waluty na jaką ma być przeliczany portfel:")
                currency = input()
                correct = czy_poprawna_nazwa_waluty(currency)
            change_main_currency(currency)
            print("GOTOWE!\n\n\n")
        elif choice == "2":
            correct = False
            while not correct:
                print("Podaj skrót waluty jaką chcesz dodać: ")
                currency = input()
                correct = czy_poprawna_nazwa_waluty(currency)
            print("Podaj ilość waluty do dodania: ")
            quantity = input()
            quantity = int(quantity)
            change_resources_in_wallet("add", currency, quantity)
            print("GOTOWE!\n\n\n")
        elif choice == "3":
            correct = False
            while not correct:
                print("Podaj skrót waluty jaką chcesz usunąć: ")
                currency = input()
                correct = czy_poprawna_nazwa_waluty(currency)
            change_resources_in_wallet("remove", currency)
            print("GOTOWE!\n\n\n")
        elif choice == "4":
            correct = False
            while not correct:
                print("Podaj skrót waluty jaką chcesz zmienić: ")
                currency = input()
                correct = czy_poprawna_nazwa_waluty(currency)
            print("Podaj ilość waluty jaka ma być w portfelu: ")
            quantity = input()
            quantity = int(quantity)
            change_resources_in_wallet("change", currency, quantity)
            print("GOTOWE!\n\n\n")
        elif choice == "5":
            get_wallet_value()
            print("\n\n\n")
        elif choice == "6":
            correct = False
            while not correct:
                print("Podaj nazwę giełdy 'Bitbay','Bittrex','Bitstamp': ")
                name = input()
                if name == "Bitbay" or name == "Bittrex" or name == "Bitstamp":
                    correct = True
            available_currency_pairs(name)
            print("\n\n\n")
        elif choice == "7":
            end = True


def main():
    run()


if __name__ == '__main__':
    main()