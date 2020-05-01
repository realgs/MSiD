import Stocks
import time
import algoritm
import sqlite3

trading_pairs = [
    "BTC-USD",
    "LTC-USD",
    "ETH-USD",
    "XRP-USD"
]

cryptos_in_order = [
    "BTC",
    "LTC",
    "ETH",
    "XRP"
]


def fetch_data():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM data')
    data = cursor.fetchall()
    return data


def extract_prices(data, trading_pair):
    prices = []
    for (date, price, exchange) in data:
        if exchange == trading_pair:
            prices.append(price)
    return prices


class DecisionAgent:

    def __init__(self):
        self.cryptos = {
            'BTC': 1,
            'LTC': 1,
            'ETH': 1,
            'XRP': 1
        }
        self.USD = 10000
        self.data = fetch_data()

    def get_current_richness_estimate(self):
        crypto_val = 0
        for pair_index in range(4):
            crypto_val += self.cryptos[cryptos_in_order[pair_index]] * Stocks.get_current_currency_value('bitbay',
                                                                                                         pair_index)
        return self.USD + crypto_val

    def buy(self, pair_index, amount_spent):
        (bid, ask) = Stocks.consider_commisons('bitbay', Stocks.get_sells_and_buys('bitbay', pair_index))
        amount = amount_spent / ask
        self.USD -= amount_spent
        self.cryptos[cryptos_in_order[pair_index]] += amount
        print(f"Bought {amount} {cryptos_in_order[pair_index]} for {amount_spent} USD")

    def sell(self, pair_index, amount):
        (bid, ask) = Stocks.consider_commisons('bitbay', Stocks.get_sells_and_buys('bitbay', pair_index))
        self.cryptos[cryptos_in_order[pair_index]] -= amount
        self.USD += amount * bid
        print(f"Sold {amount} {cryptos_in_order[pair_index]} for {amount * bid} USD")

    def make_transaction(self):
        for pair_index in range(4):
            decision = algoritm.decide_if_buy_or_sell(extract_prices(self.data, trading_pairs[pair_index]),
                                                      Stocks.get_current_currency_value('bitbay', pair_index))
            buy_amount = self.USD
            sell_amount = self.cryptos[cryptos_in_order[pair_index]] / 5
            if decision == 'BUY' and buy_amount > 0:
                self.buy(pair_index, buy_amount)
                print(f"Current richness {self.get_current_richness_estimate()}")
            elif decision == 'SELL' and sell_amount > 0:
                self.sell(pair_index, sell_amount)
                print(f"Current richness {self.get_current_richness_estimate()}")


    def go(self):
        print(f"Current richness {self.get_current_richness_estimate()}")
        while True:
            self.make_transaction()
            time.sleep(60)


if __name__ == '__main__':
    ag = DecisionAgent()
    ag.go()
