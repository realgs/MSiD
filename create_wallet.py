import sqlite3
import os

def create_database(path):
    if os.path.exists(path):
        os.remove(path)
        print("The old database has been delated, it will be replaced by a new one.")
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(""" CREATE TABLE wallet (
            currency text,
            amount double
    )""")
    connection.commit()
    connection.close()
    print("The new database has been created.")

if __name__ == "__main__":
    create_database()