import time
import requests


def search_market(market_currency, base_currency):
    market_currency = market_currency.upper()
    base_currency = base_currency.upper()
    markets = requests.get("https://api.bittrex.com/api/v1.1/public/getmarkets")
    markets_json = markets.json()
    if markets_json["success"]:
        markets_records = markets_json["result"]
        for record in markets_records:
            if (record["MarketCurrency"] == market_currency or ["MarketCurrencyLong"] == market_currency) and (
                    record["BaseCurrency"] == base_currency or record["BaseCurrencyLong"] == base_currency):
                return record
    else:
        print('Nie udało się pobrać "markets" !')


def transaction_history(market_currency, base_currency, amount_orders):
    market = search_market(market_currency, base_currency)
    if market is not None:
        name_of_market_currency = market["MarketCurrency"].upper()
        name_of_base_currency = market["BaseCurrency"].upper()
        last_transaction = requests.get("https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=" +
                                        name_of_base_currency + "-" + name_of_market_currency)
        last_transaction_json = last_transaction.json()
        print("Ostatnie oferty kupna " + name_of_base_currency + "-" + name_of_market_currency + ":")
        number_of_transactions_downloaded = 0
        list_of_recent_purchase_offers = []
        current_line = 0
        while number_of_transactions_downloaded != amount_orders and current_line != len(last_transaction_json["result"]):
            if last_transaction_json["result"][current_line]["OrderType"] == "BUY":
                list_of_recent_purchase_offers.append((last_transaction_json["result"][current_line]["Price"],
                                                 last_transaction_json["result"][current_line]["Quantity"]))
                print("\t" + str(list_of_recent_purchase_offers[number_of_transactions_downloaded][0]) + " (qty: " +
                      str(list_of_recent_purchase_offers[number_of_transactions_downloaded][1]) + ")")
                number_of_transactions_downloaded += 1
            current_line += 1

        print("Ostatnie oferty sprzedaży " + name_of_base_currency + "-" + name_of_market_currency + ":")
        number_of_transactions_downloaded = 0
        list_of_recent_sales_offers = []
        current_line = 0
        while number_of_transactions_downloaded != amount_orders and current_line != len(last_transaction_json["result"]):
            if last_transaction_json["result"][current_line]["OrderType"] == "SELL":
                list_of_recent_sales_offers.append((last_transaction_json["result"][current_line]["Price"],
                                                        last_transaction_json["result"][current_line]["Quantity"]))
                print("\t" + str(list_of_recent_sales_offers[number_of_transactions_downloaded][0]) + " (qty: " +
                      str(list_of_recent_sales_offers[number_of_transactions_downloaded][1]) + ")")
                number_of_transactions_downloaded += 1
            current_line += 1
        return list_of_recent_purchase_offers, list_of_recent_sales_offers
    else:
        print("Podana kombinacja walut nie istnieje na ryneczku :(")


def auto_transaction_history(market_currency, base_currency, amount_orders, time_period):
    print("\nTrwa uruchamianie automatycznego wypisu danych z rynku \n")
    market = search_market(market_currency, base_currency)
    if market is not None:
        name_of_market_currency = market["MarketCurrency"].upper()
        name_of_base_currency = market["BaseCurrency"].upper()
    else:
        print("Podana kombinacja walut nie istnieje na ryneczku :(")
    while market is not None:
        list_of_recent_purchase_offers, list_of_recent_sales_offers = transaction_history(market_currency, base_currency, amount_orders)
        if len(list_of_recent_purchase_offers) >= len(list_of_recent_sales_offers):
            max_number_of_differences = len(list_of_recent_sales_offers)
        else:
            max_number_of_differences = len(list_of_recent_purchase_offers)
        print("Różnica między kupnem, a sprzedażą " + name_of_base_currency + "-" + name_of_market_currency + ":")
        for i in range(max_number_of_differences):
            print("\t" + str((1 - (list_of_recent_sales_offers[i][0] - list_of_recent_purchase_offers[i][0]) /
                             list_of_recent_sales_offers[i][0])*100) + "%")
        print("\n")
        time.sleep(time_period)


def main():
    transaction_history("ETH", "UsD", 15)
    auto_transaction_history("ETH", "USD", 10, 5)


if __name__ == '__main__':
    main()
