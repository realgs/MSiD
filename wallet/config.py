import _sqlite3
db_wallet = _sqlite3.connect('walet_resource.db')
sql_cursor = db_wallet.cursor()

sql_cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    crypto_name TEXT,
    quantity INTEGER
    )""")

db_wallet.commit()