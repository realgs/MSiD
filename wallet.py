import csv
import api
import tkinter.messagebox

DEFAULT_CURRENCY = 'USD'
FILENAME = 'wallet.csv'


def read_wallet_data():
    try:
        csv_wallet = []
        csv_file = open(FILENAME, 'r')
        with csv_file:
            csv_reader = csv.reader(csv_file, dialect='semicolons')
            for row in csv_reader:
                try:
                    if len(row) == 2:
                        currency = row[0]
                        amount = float(row[1])
                        csv_wallet.append((currency, amount))
                except ValueError:
                    pass
            csv_file.close()
            return csv_wallet
    except FileNotFoundError:
        tkinter.messagebox.showinfo('Error', 'Something went wrong. Check if your file is exist.')
        return []


def convert_wallet(wallet, converting_currency):
    wallet_money = 0
    for currency in wallet:
        wallet_currency_name = currency[0]
        quantity = currency[1]

        offers = []
        for api_name in api.API_NAMES:
            offers += api.get_orderbook(converting_currency, wallet_currency_name, api_name)

        if len(offers) == 0:
            if wallet_currency_name.upper() == converting_currency.upper():
                wallet_money += quantity
                continue
            print(f"{wallet_currency_name.upper()}-{converting_currency.upper()} is not available in API")
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

    # print('Totally you have', str(wallet_money), converting_currency, 'in your wallet.')
    return_str = 'Totally you have ' + str(wallet_money) + ' ' + converting_currency + ' in your wallet.'
    return return_str


def save_wallet_to_file(wallet):
    csv.register_dialect('semicolons', delimiter=';')

    file = open(FILENAME, 'w+')
    with file:
        writer = csv.writer(file, dialect='semicolons')
        writer.writerow(('Currency', 'Quantity'))

        for currency in wallet:
            writer.writerow((currency[0].upper(), currency[1]))


def remove_currency(currency_to_remove, wallet):
    for currency in wallet:
        if currency[0] == currency_to_remove:
            wallet.remove(currency)
    save_wallet_to_file(wallet)


def add_currency(currency_name, amount, wallet):
    currency_exist = False
    currency_name = currency_name
    for currency in wallet:
        if currency[0] == currency_name:
            remove_currency(currency_name, wallet)
            wallet.append((currency_name, amount))
            currency_exist = True
            break
    if not currency_exist:
        wallet.append((currency_name, amount))

    save_wallet_to_file(wallet)


def edit_currency_amount(currency_name, new_amount, wallet):
    remove_currency(currency_name, wallet)
    add_currency(currency_name, new_amount, wallet)


def check_currency_in_wallet(currency_name, wallet):
    for currency in wallet:
        if currency[0] == currency_name:
            return True
    return False


def add_currency_amount(currency_name, amount_to_add, wallet):
    currency_exist = False
    currency_name = currency_name
    for currency in wallet:
        if currency[0] == currency_name:
            currency_amount = currency[1] + amount_to_add
            remove_currency(currency_name, wallet)
            wallet.append((currency_name, currency_amount))
            currency_exist = True
            save_wallet_to_file(wallet)
            break
    if not currency_exist:
        print('In your wallet there is no such currency. :(')


def print_wallet(wallet):
    wallet_str = ''
    for currency in wallet:
        wallet_str += str(currency[0]) + ' ' + str(currency[1]) + '\n'
    return wallet_str
