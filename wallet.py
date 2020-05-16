import sqlite3
import apiBroker


class Wallet:
    def __init__(self, base, database):
        self.database = database
        self.wallet = dict()
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.load_wallet()

    def load_wallet(self):
        self.cursor.execute('SELECT * FROM wallet')
        self.wallet.update(self.cursor.fetchall())

    def add_resources(self, resource, amount):
        self.wallet[resource] += amount
        self.save_wallet()

    def remove_resources(self, resource, amount):
        self.wallet[resource] -= amount
        self.save_wallet()

    def set_resource_state(self, resource, amount):
        self.wallet[resource] = amount
        self.save_wallet()

    def save_wallet(self):
        for resource in self.wallet:
            self.cursor.execute('''UPDATE wallet
                                SET amount = ?
                                WHERE resource = ?''',
                                (self.wallet[resource], resource))
            self.connection.commit()

    def remove_resource_from_wallet(self, resource):
        self.cursor.execute(
            '''DELETE FROM wallet
                WHERE resource = ?''',
            [resource]
        )
        self.connection.commit()

    def add_new_resource(self, resource, base_amount=0):
        if apiBroker.api_supports_resource(resource):
            self.wallet[resource] = base_amount
            self.cursor.execute("INSERT INTO wallet VALUES (?,?)", (resource, base_amount))
            self.connection.commit()
        else:
            print(f"API does not support cryptocurrency: {resource}")

    def eval_wallet_value(self, currency):
        total_value = 0
        print(f"Evaluating wallet value in {currency}:")
        for resource in self.wallet:
            if resource == currency:
                val = self.wallet[resource]
            else:
                val = apiBroker.evalValue(currency, resource, self.wallet[resource])
            if val is None:
                print(f"{resource} : trading for {currency} is not possible on the market")
            else:
                print(f"{resource} : {val}")
                total_value += val
        print(f"Total wallet value in {currency}: {total_value}")


if __name__ == '__main__':
    pass
