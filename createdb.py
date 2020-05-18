import sqlite3
import os


if os.path.exists("data.db"):
    os.remove("data.db")
    print("Old database removed.")
connection = sqlite3.connect("data.db")
cursor = connection.cursor()
cursor.execute('''CREATE TABLE data
             (date text, price real, pair text)''')
connection.commit()
connection.close()
print("New database created.")
