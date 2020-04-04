import requests
import time


trades = None


def update_trades(crypto_currency, currency):
    global trades
    try:
        request = requests.get(
            f"https://bitbay.net/API/Public/{crypto_currency}{currency}/orderbook.json"
        )
        trades = request.json()
    except requests.exceptions.RequestException as e:
        trades = None
        print(e)


def print_values(lines):
    for i in range(0, lines):
        bid = trades["bids"][i][0]
        ask = trades["asks"][i][0]
        print(f"{bid:>-10}    {ask:>-10}    {((ask - bid) / bid):>-.5f}%")


def analysis(crypto_type, currency_type, lines):
    update_trades(crypto_type, currency_type)
    if trades is not None:
        print_values(lines)
        print("\n")
    else:
        print("Error")
    time.sleep(5)


def main():
    while True:
        analysis("eth", "pln", 10)


if __name__ == '__main__':
    main()