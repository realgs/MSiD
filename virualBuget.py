

class VirtualBudget:
    def __init__(self, money):
        self.startingMoney = money
        self.currentMoney = money

    def make_transaction(self, buy_price, sell_price):
        amount_bought = self.currentMoney / buy_price
        money_earned = (amount_bought * sell_price) - (amount_bought * buy_price)
        self.currentMoney += money_earned

    def print_budget(self):
        print(f"My current budget state: {self.currentMoney}")