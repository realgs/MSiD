import sqlite3


def api_supports_resource():
    return True  # check if api supports give resource


class Wallet:
    def __init__(self, base, database):
        self.baseCurrency = base
        self.database = database
        self.wallet = dict()
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.load_wallet()

    def load_wallet(self):
        self.cursor.execute('SELECT * FROM wallet') #or whatever the hell will it be
        self.wallet.update(self.cursor.fetchall())


    def set_base_currency(self, base):
        self.baseCurrency = base

    def add_resources(self, resource, amount):
        self.wallet[resource] += amount
       # self.save_wallet_state()

    def remove_resources(self, resource, amount):
        self.wallet[resource] -= amount
      #  self.save_wallet_state()

    def set_resource_state(self, resource, amount):
        self.wallet[resource] = amount

    def save_wallet(self):
        for resource in self.wallet:
            self.cursor.execute('''UPDATE wallet
                                SET amount = ?
                                WHERE resource = ?''',
                                self.wallet[resource], resource)

    def add_new_resource(self, resource, base_amount=0):
        self.wallet[resource] = base_amount
        self.cursor.execute("INSERT INTO wallet VALUES (?,?)", (resource, base_amount))
        self.connection.commit()