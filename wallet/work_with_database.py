import _sqlite3
def createDataBase():
    db_wallet = _sqlite3.connect('walet_resource.db')
    sql_cursor = db_wallet.cursor()
    sql_cursor.execute("""CREATE TABLE IF NOT EXISTS crypto (crypto_name TEXT,
                                                             quantity INTEGER
                                                             )""")
    db_wallet.commit()
    sql_cursor.close()
    db_wallet.close()
#havent checked\'
def addNewValue(currency, quantity):
    db_wallet = _sqlite3.connect('walet_resource.db')
    sql_cursor = db_wallet.cursor()
    list_to_add = [currency, quantity]
    sql_cursor.execute("""INSERT INTO crypto VALUES(?, ?)""", list_to_add)
    db_wallet.commit()
    sql_cursor.close()
    db_wallet.close()
def printTable():
    db_wallet = _sqlite3.connect('walet_resource.db')
    sql_cursor = db_wallet.cursor()
    for row in sql_cursor.execute('SELECT * FROM crypto'):
        print(row)
    db_wallet.commit()
    sql_cursor.close()
    db_wallet.close
def ifExistCryptoInDB(currency):
    db_wallet = _sqlite3.connect('walet_resource.db')
    sql_cursor = db_wallet.cursor()
    list = sql_cursor.execute("""SELECT COUNT(*) FROM crypto WHERE crypto_name =?""", [currency])
    to_ret = False
    for line in list:#one line, cause of it gives num of exists
        if(line[0] == 0):
            to_ret = False
        else:
            to_ret = True
        db_wallet.commit()
        sql_cursor.close()
        db_wallet.close
        return to_ret
createDataBase()
print(ifExistCryptoInDB("ETH"))

