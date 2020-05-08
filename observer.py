import time
import requests


def get_bittrex_orderbook(market_currency, base_currency):
    market_currency = market_currency.upper()
    base_currency = base_currency.upper()
    orderbook = requests.get("https://api.bittrex.com/api/v1.1/public/getorderbook?market=" + market_currency + "-"
                             + base_currency + "&type=both")
    orderbook_json = orderbook.json()
    if orderbook_json["success"]:
        buy = orderbook_json["result"]["buy"][0]
        sell = orderbook_json["result"]["sell"][0]
        result = ["bittrex",buy["Quantity"], buy["Rate"], sell["Quantity"], sell["Rate"]]
        print(result)
        return result

def get_bitbay_orderbook(market_currency, base_currency):
    market_currency = market_currency.upper()
    base_currency = base_currency.upper()
    orderbook = requests.get("https://bitbay.net/API/Public/" + market_currency + base_currency
                             + "/orderbook.json")
    orderbook_json = orderbook.json()
    buy = orderbook_json["bids"][0]
    sell = orderbook_json["asks"][0]
    result = ["bitbay", buy[1], buy[0], sell[1], sell[0]]
    print(result)
    return result


def get_bitstamp_orderbook(market_currency, base_currency):
    market_currency = market_currency.lower()
    base_currency = base_currency.lower()
    orderbook = requests.get("https://www.bitstamp.net/api/v2/order_book/" + market_currency + base_currency
                             + "/")
    orderbook_json = orderbook.json()
    buy = orderbook_json["bids"][0]
    sell = orderbook_json["asks"][0]
    result = ["bitstamp", buy[1], buy[0], sell[1], sell[0]]
    print(result)
    return result


def get_bitclude_orderbook(market_currency, base_currency):
    market_currency = market_currency.lower()
    base_currency = base_currency.lower()
    orderbook = requests.get("https://api.bitclude.com/stats/orderbook_" + market_currency + base_currency
                             + ".json")
    orderbook_json = orderbook.json()
    buy = orderbook_json["bids"][0]
    sell = orderbook_json["asks"][0]
    result = ["bitclude", buy[0], buy[1], sell[0], sell[1]]
    print(result)
    return result


def main():
    get_bittrex_orderbook("BTC", "LTC")
    get_bitbay_orderbook("LTC", "BTC")
    get_bitstamp_orderbook("LTC", "BTC")
    get_bitclude_orderbook("LTC", "BTC")


if __name__ == '__main__':
    main()
