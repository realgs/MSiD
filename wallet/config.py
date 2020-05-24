DB_FILE_PATH = 'walet_resource.db'
basic_currency = ''
URL_BITBAY_LAST_TRANSACTIONS = "https://api.bitbay.net/rest/trading/transactions/"#last transactions
#I CANT YOUSE LAST TRANSACTIONS, CAUSE API GIVES LAST 10 AND THERE CAN BE ONLY TRANSACTIONS OF ONE TYPE. That's why i propose to use orderbook.
#ALSO IT WILL SIMPLIFY ALGORITHM OF FINDING COURSE. CAUSE I NEED TO TAKE THE FIRST BEST PROPOSITION AND IT IS SORTED
URL_BITBAY_ORDERBOOK = "https://api.bitbay.net/rest/trading/orderbook/"
URL_BITBAY_TICKER = "https://api.bitbay.net/rest/trading/stats" #all currencies propositions
LIST_BITBAY_ARGS = ["BTC-USD", "BTC-EUR", "LTC-BTC", "ETH-USD"]
BASIC_CURRENCIES = ["USD", "PLN", "EUR"]