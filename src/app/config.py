MARKET_CURRENCY_MAPPING = {
    'BTC-USD': 'BTC',
    'LTC-USD': 'LTC',
    'ETH-USD': 'ETH',
    'XRP-USD': 'XRP',
}

INITIAL_WALLET = {
    'USD': 3000,
    'BTC': 0,
    'LTC': 0,
    'ETH': 0,
    'XRP': 0,
}


MARKETS = list(MARKET_CURRENCY_MAPPING.keys())
TRADE_CURRENCIES = list(MARKET_CURRENCY_MAPPING.values())
CURRENCIES = list(INITIAL_WALLET.keys())

TRADING_FEE = 0.0010

BITBAY_API_URL = 'https://api.bitbay.net/rest/trading/ticker/'

