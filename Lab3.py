import requests


def search_market(market_currency, base_currency):
    market_currency = market_currency.upper()
    base_currency = base_currency.upper()
    markets = requests.get("https://api.bittrex.com/api/v1.1/public/getmarkets")
    markets_json = markets.json()
    if markets_json["success"]:
        print("Udalo się pobrać \"markets\" !")
        markets_records = markets_json["result"]
        for record in markets_records:
            if (record["MarketCurrency"] == market_currency or ["MarketCurrencyLong"] == market_currency) and (
                    record["BaseCurrency"] == base_currency or record["BaseCurrencyLong"] == base_currency):
                return record
    else:
        print("Nie udało się pobrać \"markets\" !")


def transaction_history(market_currency, base_currency, amount_orders):
    market = search_market(market_currency, base_currency)
    name_of_market_currency = market["MarketCurrency"]
    name_of_base_currency = market["BaseCurrency"]
    if market is not None:
        last_transaction = requests.get("https://api.bittrex.com/api/v1.1/public/getorderbook?market=" +
                                        name_of_base_currency + "-" + name_of_market_currency + "&type=both")
        last_transaction_json = last_transaction.json()
        print("Ostatnie oferty kupna " + name_of_base_currency + "-" + name_of_market_currency + ":")
        for i in range(amount_orders):
            print("\t" + str(last_transaction_json["result"]["buy"][i]["Rate"]))
        print("Ostatnie oferty sprzedaży " + name_of_base_currency + "-" + name_of_market_currency + ":")
        for i in range(amount_orders):
            print("\t" + str(last_transaction_json["result"]["sell"][i]["Rate"]))
    else:
        print("Podana kombinacja walut nie istnieje na ryneczku :(")


def main():
    transaction_history("ETH", "USD", 5)


if __name__ == '__main__':
    main()