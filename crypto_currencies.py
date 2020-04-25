import json
import requests


def get_url_data(url):
    try:
        request = requests.get(url)
        data = json.loads(request.text)
        return data
    except requests.exceptions.ConnectionError:
        print("No connection")
        return None


def create_market_url(currencies):
    return 'https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=' + currencies.upper()


def print_offers(crypto_currencies, offers_amount=100):
    url = create_market_url(crypto_currencies)

    data = get_url_data(url)
    if data is None:
        return
    elif data["success"] is False:
        print("Wrong url: " + url)
        return

    print("\ncurrency offers: " + crypto_currencies.upper())
    print("Buy offers:")
    start_print_loop(data, "buy", offers_amount)

    print("\nSell offers:")
    start_print_loop(data, "sell", offers_amount)


def start_print_loop(data, result_arg, offers_amount=100):
    if result_arg.upper() != "BUY" and result_arg.upper() != "SELL":
        print("Wrong argument:", result_arg)
        return

    counter = 0
    for offer in data["result"]:
        if offer['OrderType'] == result_arg.upper():
            print_single_offer(offer)
            counter += 1
            if counter == offers_amount:
                break


def print_single_offer(offer):
    print("Quantity:", end=" ")
    print("{0:15}".format(str(offer["Quantity"])), end=" | ")
    print("Price:", offer["Price"])


def main():
    crypto_currencies = ['btc-eth', 'btc-ltc', 'eth-ltc']

    for currencies in crypto_currencies:
        print_offers(currencies, offers_amount=3)


if __name__ == "__main__":
    main()
