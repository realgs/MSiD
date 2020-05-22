import _sqlite3
import config
def createDataBase():
    getDataBDByRequest("""CREATE TABLE IF NOT EXISTS crypto (crypto_name TEXT,
                                                             quantity INTEGER
                                                             )""", [])

def addNewValue(currency, quantity):
    getDataBDByRequest("""INSERT INTO crypto VALUES(?, ?)""", [currency, quantity])

def printTable():
    tableToPrint = getDataBDByRequest('SELECT * FROM crypto', [])
    for line in tableToPrint:
        print(line)

def ifExistCryptoInDB(currency):
    getDataBDByRequest("""SELECT COUNT(*) FROM crypto WHERE crypto_name =?""", [currency])
    countRecordsBD = getDataBDByRequest("""SELECT COUNT(*) FROM crypto WHERE crypto_name =?""", [currency])[0][0]
    if(countRecordsBD > 0):
        return True
    else:
        return False

def getCryptoQuantityByName(currency):
    if not ifExistCryptoInDB(currency):
        return 0
    else:
        quantity = getDataBDByRequest("""SELECT quantity FROM crypto WHERE crypto_name = ?""", [currency])[0][0]
        return quantity

def getDataBDByRequest(request, arrayArgs):
    db_wallet = _sqlite3.connect(config.DB_FILE_PATH)
    sql_cursor = db_wallet.cursor()
    dDResult = sql_cursor.execute(request, arrayArgs)
    objDB = dDResult.fetchall()
    db_wallet.commit()
    sql_cursor.close()
    db_wallet.close()
    return objDB

createDataBase()
print(ifExistCryptoInDB("USD"))
getCryptoQuantityByName("USD")
ifExistCryptoInDB("USD")
printTable()