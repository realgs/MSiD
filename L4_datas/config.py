#URL_BITBAY = "https://api.bitbay.net/rest/trading/orderbook/BTC-USD"
#EXAMLE URL_BITTREX = "https://api.bittrex.com/api/v1.1/public/getorderbook?market=USD-BTC&type=both"

URL_BITTREX_FIRST_P = "https://api.bittrex.com/api/v1.1/public/getorderbook?market="
URL_BITTREX_SECOND_P = "&type=both"
URL_BITBAY = "https://api.bitbay.net/rest/trading/orderbook/"

#potrzebuje tabele bo parametry w odwrotnej kolejności
LIST_BITBAY_ARGS = ["BTC-USD", "BTC-EUR", "LTC-BTC", "ETH-USD"]
LIST_BITTREX_ARGS = ["USD-BTC", "EUR-BTC", "BTC-LTC", "USD-ETH"]

LISTS_LENGTH_HELPER = [0,1,2,3]

BITTBAY_SELLER_BITTREX_BUYER = 0
BITTREX_SELLER_BITBAY_BUYER = 1

MAX_TAKER_BITBAY = 0.043
MIN_TAKER_BITBAY = 0.025
TAKER_BITTREX = 0.2

LINK_INFO_BITBAY = "https://bitbay.net/en/helpdesk/exchange/what-is-maker-and-taker-fee"
LINK_INFO_BITTREX = "https://bittrex.zendesk.com/hc/en-us/articles/115000199651-What-fees-does-Bittrex-charge-"