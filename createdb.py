import sqlite3
import os


if os.path.exists("wallet.db"):
    os.remove("wallet.db")
    print("Old database removed.")
connection = sqlite3.connect("wallet.db")
cursor = connection.cursor()
cursor.execute('''CREATE TABLE wallet
             (resource text PRIMARY KEY, amount real)''')
connection.commit()
connection.close()
print("New database created.")
