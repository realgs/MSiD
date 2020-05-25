import csv
import json
import requests


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

                            wallet.append((currency_name, quantity))
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

            price = get_currency_price(currency_name, wallet_currency_name)
            if price == 0:
                print("Currency is not available in bittrex API")
                return None

            wallet_money += quantity * price

        return wallet_money

    def print_wallet_currencies(self):
        for currency in self.__wallet:
            print(currency[0], currency[1])

    def add_currency(self, currency_name, quantity):
        pass

    def remove_currency(self, currency_name):
        pass

    def edit_currency_quantity(self, currency_name, new_quantity):
        pass


def get_url_data(url):
    try:
        request = requests.get(url)
        data = json.loads(request.text)
        return data
    except requests.exceptions.ConnectionError:
        print("No connection")
        return None


def get_currency_price(base_currency, exchange_currency):
    data = get_url_data('https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=' + base_currency + '-' +
                        exchange_currency)

    for offer in data["result"]:
        if offer['OrderType'] == "BUY":
            return offer['Price']

    return 0


def currency_available_in_api(base_currency, exchange_currency):
    data = get_url_data('https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=' + base_currency + '-' +
                        exchange_currency)
    return data["success"]


def enter_wallet_data(filename, wallet_currency):
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
            if currency_available_in_api(wallet_currency, currency):
                writer.writerow((currency, quantity))
            else:
                print("Currency is not available in api")

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
    my_money = wallet.calculate_wallet_money(wallet_currency)
    wallet.print_wallet_currencies()
    print(my_money, wallet_currency.upper())


if __name__ == "__main__":
    main()
