import requests

base_currency = None
wallet={}

available_currencies = set()


def get_currencies_data():
    currencies_bittrex = requests.get("https://api.bittrex.com/api/v1.1/public/getcurrencies")
    currencies_bittrex_json = currencies_bittrex.json()
    for currency_info in currencies_bittrex_json['result']:
        # print(currency_info['Currency'])
        available_currencies.add(currency_info['Currency'])
    print(available_currencies)
    print(len(available_currencies))


def set_base_currency():
    currency = input("Type in base currency of your wallet: ")
    global base_currency
    base_currency = currency

def check_market_availability(base_currency,currency):
    orderbook = requests.get(
        "https://api.bittrex.com/api/v1.1/public/getorderbook?market={0}-{1}&type=both".format(base_currency, currency))
    orderbook_json = orderbook.json()
    return orderbook_json['success']

def add_wallet_data(currency, amount):
    if check_market_availability(base_currency,currency):
        if currency in wallet.keys():
            wallet[currency] += amount
        else:
            wallet[currency] = amount
    else:
        print("{0}-{1} market isn't available".format(base_currency,currency))


def wallet_data_input():
    try:
        currency = input("Type in name of currency to add: ")
        amount=float(input("Type in amount of this currency: "))
    except ValueError:
        print("This is not a valid amount")
    print(currency)
    print(amount)
    add_wallet_data(currency,amount)

def main():
    set_base_currency()
    #get_currencies_data()
    #print(base_currency)
    wallet_data_input()
    #wallet_data_input()
    print(wallet)


if __name__ == "__main__":
    main()
