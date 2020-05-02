import Stocks
import time
import algoritm
import sqlite3
import datagatherer

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
    datagatherer.gather_data()
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
            'BTC': 0,
            'LTC': 0,
            'ETH': 0,
            'XRP': 0
        }
        self.USD = 100000
        self.data = fetch_data()

    #wealthness = current estimated value of cryptos as if they were sold in this moment in USD + USD left
    def get_current_wealthness_estimate(self):
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
            self.data = fetch_data()
            decision = algoritm.decide_if_buy_or_sell(extract_prices(self.data, trading_pairs[pair_index]),
                                                      Stocks.get_current_currency_value('bitbay', pair_index))

            diff_percent = algoritm.get_diff_percent(extract_prices(self.data, trading_pairs[pair_index]),
                                                      Stocks.get_current_currency_value('bitbay', pair_index))

            buy_amount = self.USD * diff_percent
            sell_amount = self.cryptos[cryptos_in_order[pair_index]] * diff_percent
            if decision == 'BUY' and buy_amount > 0:
                self.buy(pair_index, buy_amount)
                print(f"Current wealthness {self.get_current_wealthness_estimate()}")
            elif decision == 'SELL' and sell_amount > 0:
                self.sell(pair_index, sell_amount)
                print(f"Current wealthness {self.get_current_wealthness_estimate()}")

    def run(self):
        print(f"Current wealthness {self.get_current_wealthness_estimate()}")
        while True:
            self.make_transaction()
            time.sleep(1200)


if __name__ == '__main__':
    ag = DecisionAgent()
    #buy some starting cryptos
    ag.buy(0, 2000)
    ag.buy(1, 2000)
    ag.buy(2, 2000)
    ag.buy(3, 2000)
    ag.run()
