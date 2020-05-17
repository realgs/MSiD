import sqlite3
import os

def create_database(path):
    if os.path.exists(path):
        os.remove(path)
        print("An old database removed.")
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(""" CREATE TABLE wallet_data (
            currency text,
            amount double
    )""")
    cursor.execute(""" CREATE TABLE currency_data (
                base_currency text,
                currency text,
                source text
    )""")
    connection.commit()
    connection.close()
    print("The new database created.")

if __name__ == "__main__":
    create_database()