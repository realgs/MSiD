import csv
import json
from json import JSONDecodeError

import requests

api_names = ['bitbay', 'bittrex', 'cex']


class Wallet:
    def __init__(self, wallet_filename):
        self.__filename = wallet_filename
        self.__wallet = self.__read_wallet_data()

    def __read_wallet_data(self):
        try:
            file = open(self.__filename, "r")
            wallet = []

            with file:
                reader = csv.reader(file, dialect='semicolons')
                for row in reader:
                    try:
                        if len(row) == 2:
                            quantity = float(row[1])
                            currency_name = row[0]

                            wallet.append((currency_name.upper(), quantity))
                    except ValueError:
                        pass
                file.close()
                return wallet
        except FileNotFoundError:
            print("File doesn't exist")
            return []

    def calculate_wallet_money(self, currency_name):
        wallet_money = 0
        for currency in self.__wallet:
            wallet_currency_name = currency[0]
            quantity = currency[1]

            offers = []
            for api in api_names:
                offers += get_buy_data(currency_name, wallet_currency_name, api)

            if len(offers) == 0:
                if wallet_currency_name.upper() == currency_name.upper():
                    wallet_money += quantity
                    continue
                print(f"{wallet_currency_name.upper()}-{currency_name.upper()} is not available in API")
                return None

            price = lambda currency_offer: currency_offer[1]
            offers.sort(key=price, reverse=True)

            for offer in offers:
                offer_quantity = offer[0]
                offer_price = offer[1]
                if offer_quantity >= quantity:
                    wallet_money += offer_price * quantity
                    quantity = 0
                else:
                    wallet_money += offer_price * offer_quantity
                    quantity -= offer_quantity

                if quantity == 0:
                    break

            if quantity > 0:
                print(f"There is not enough buy offers on markets for {currency}")

        return wallet_money

    def print_wallet_currencies(self):
        for currency in self.__wallet:
            print(currency[0], currency[1])

    def add_currency(self, currency_name, quantity):
        currency_exist = False
        currency_name = currency_name.upper()
        for currency in self.__wallet:
            if currency[0].upper() == currency_name:
                currency_quantity = currency[1]
                self.remove_currency(currency_name)
                self.__wallet.append((currency_name, quantity + currency_quantity))
                currency_exist = True
                break
        if not currency_exist:
            self.__wallet.append((currency_name, quantity))

        self.__save_wallet_to_file()

    def remove_currency(self, currency_name):
        for currency in self.__wallet:
            if currency[0].upper() == currency_name.upper():
                self.__wallet.remove(currency)
        self.__save_wallet_to_file()

    def edit_currency_quantity(self, currency_name, new_quantity):
        self.remove_currency(currency_name)
        self.add_currency(currency_name, new_quantity)

    def __save_wallet_to_file(self):
        csv.register_dialect('semicolons', delimiter=';')

        file = open(self.__filename, 'w+')
        with file:
            writer = csv.writer(file, dialect='semicolons')
            writer.writerow(('Currency', 'Quantity'))

            for currency in self.__wallet:
                writer.writerow((currency[0].upper(), currency[1]))


def get_url_data(url):
    try:
        request = requests.get(url)
        data = json.loads(request.text)
        return data
    except requests.exceptions.ConnectionError:
        print("No connection")
        return None


def create_market_url(base_currency, exchange_currency, api_name):
    base_currency = base_currency.upper()
    exchange_currency = exchange_currency.upper()

    if api_name == 'bittrex':
        return f'https://api.bittrex.com/api/v1.1/public/getorderbook?market={base_currency}-' \
               f'{exchange_currency}&type=both'
    if api_name == 'bitbay':
        return f'https://bitbay.net/API/Public/{exchange_currency}{base_currency}/orderbook.json'
    if api_name == 'cex':
        return f'https://cex.io/api/order_book/{exchange_currency}/{base_currency}'


def get_buy_data(base_currency, exchange_currency, api_name):
    data = get_url_data(create_market_url(base_currency, exchange_currency, api_name))
    buy_offers = []

    try:
        if api_name == 'bittrex':
            for bid in data['result']['buy']:
                buy_offers.append((bid['Quantity'], bid['Rate']))

        if api_name == 'cex' or api_name == 'bitbay':
            for bid in data['bids']:
                buy_offers.append((bid[1], bid[0]))
    except TypeError:
        return []
    except KeyError:
        return []

    return buy_offers


def currencies_available_in_api(base_currency, exchange_currency):
    data = get_url_data(f'https://api.bittrex.com/api/v1.1/public/getorderbook?market={base_currency}-'
                        f'{exchange_currency}&type=both')
    if data["success"]:
        pass
        return True

    try:
        data = get_url_data(f'https://bitbay.net/API/Public/{exchange_currency}{base_currency}/orderbook.json')
        if len(data['bids']) > 0:
            pass
            return True
    except JSONDecodeError:
        pass
    except KeyError:
        pass

    try:
        data = get_url_data(f'https://cex.io/api/order_book/{exchange_currency.upper()}/{base_currency.upper()}')
        if len(data['bids']) > 0:
            return True
    except KeyError:
        pass

    return False


def enter_wallet_data(filename, currency_to_calculate):
    csv.register_dialect('semicolons', delimiter=';')

    file = open(filename, 'w+')
    with file:
        writer = csv.writer(file, dialect='semicolons')
        writer.writerow(('Currency', 'Quantity'))

        while True:
            print("Enter currency name:")
            currency = input()
            print("Enter quantity:")
            quantity = input()
            try:
                if currencies_available_in_api(currency_to_calculate, currency):
                    writer.writerow((currency, float(quantity)))
                else:
                    print("Currency is not available in API")
            except ValueError:
                print("Wrong quantity")

            print("Do you want to add next currency to the wallet? [Y/N]:")
            answer = input()
            if answer.upper() != "Y":
                break


def main():
    print("Enter the wallet currency (for example: USD): ")
    wallet_currency = input()

    filename = 'wallet.csv'
    enter_wallet_data(filename, wallet_currency)

    wallet = Wallet(filename)
    wallet_money = wallet.calculate_wallet_money(wallet_currency)
    wallet.print_wallet_currencies()
    print("Value of your wallet: ", wallet_money, wallet_currency.upper())

    wallet.add_currency('BTC', 0.73)
    wallet.print_wallet_currencies()

    wallet_money = wallet.calculate_wallet_money('BTC')
    print("Value of your wallet: ", wallet_money, 'BTC')


if __name__ == "__main__":
    main()
