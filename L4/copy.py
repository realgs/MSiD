#Najpierw zaimplementuje algorytm bioracy dane, ktorych pobieranie zaimplementuje
#pozniej

#Bedzie 16 sprawdzen czy oferta sprzedazy jest mniejsza jak oferta kupna

#Przy kalkulacjach brac pod uwage prowizje

import requests
import string
import json

markets = ['bitbay.net','bittrex.com','bitstamp.net','cex.io']

currency_pairs = [("ETH","USD"),("LTC","BTC"),("ETH","EUR"),("ETH","BTC")]

#Fees in percent values
fees = {'bitbay.net': 0.43,'bittrex.com': 0.2,'bitstamp.net': 0.5,'cex.io': 0.25}

def get_orderbook_url(market, currency_pair):
	source_currency = currency_pair[0]
	target_currency = currency_pair[1]
	if market == 'bitbay.net':
		return 'https://bitbay.net/API/Public/' + source_currency + target_currency + '/orderbook.json'
	if market == 'bittrex.com':
		return 'https://api.bittrex.com/api/v1.1/public/getorderbook?market=' + source_currency + '-' + target_currency + "&type=both"
	if market == 'bitstamp.net':
		return 'https://www.bitstamp.net/api/v2/order_book/' + source_currency.lower() + target_currency.lower() + '/'
	if market == 'cex.io':
		return 'https://cex.io/api/order_book/' + source_currency + "/" + target_currency
	return ""

def get_ticker_url(market, currency_pair):
	source_currency = currency_pair[0]
	target_currency = currency_pair[1]
	if market == 'bitstamp.net':
		return 'https://www.bitstamp.net/api/v2/ticker/' + source_currency.lower() + target_currency.lower() + '/'
	if market == 'bitbay.net':
		return 'https://bitbay.net/API/Public/' + source_currency + target_currency + '/ticker.json'
	if market == 'bittrex.com':
		return 'https://api.bittrex.com/api/v1.1/public/getticker?market=' + source_currency + '-' + target_currency
	if market == 'cex.io':
		return 'https://cex.io/api/ticker/' + source_currency + '/' + target_currency
	return ""

def getBidAskPair(market, pair):
	url = get_ticker_url(market,pair)
	req = requests.get(url)
	jsonText = req.json()
	repairedJson = str(jsonText).replace("\'", "\"")
	dict = json.loads(repairedJson)
	bid = None
	ask = None
	if 'bid' in dict.keys():
		bid = dict['bid']
	if 'ask' in dict.keys():
		ask = dict['ask']
	return (float(bid),float(ask))

def sell_offer(market, pair):
	pair = getBidAskPair(market, pair)
	return pair[1]

def buy_offer(market, pair):
	pair = getBidAskPair(market, pair)
	return pair[0]

'''
def is_arbitrage_possible():
	for pair in currency_pairs:
		#Sprawdzenie najpierw gdzie jest najmniejsza oferta sprzedazy
		best_sell_offer = [markets[0],sell_offer(markets[0],pair)]
		for market in markets:
			if market.sell_offer < best_sell_offer[1]:
				best_sell_offer[0] = market
				best_sell_offer[1] = market.sell_offer

		#Sprawdzenie gdzie jest najwieksza oferta kupna
		best_buy_offer = [market[0],markets[0].buy_offer]
		for market in markets:
			if market.buy_offer > best_buy_offer[1]:
				best_buy_offer[0] = market
				best_buy_offer[1] = market.buy_offer

		#Sprawdzenie,czy oferta kupna jest wieksza niz oferta sprzedazy

		if best_sell_offer[1] < best_buy_offer[1]:
			return(best_sell_offer,best_buy_offer)
		else:
			return None
'''
							#Sprawdza tylko czy mozna kupic na pierwszym i sprzedac na drugim, nie na odwrot
def check_arbitrage(market1, market2, curr_pair):
	sell = sell_offer(market1,pair)
	buy = buy_offer(market2,pair)
	if sell == None or buy == None:
		return False
	if buy_offer > sell_offer:
		return True
	return False

def print_arbitrages():
	for market1 in markets:
		for market2 in markets:
			for pair in currency_pairs:
				arbitrage_possible = check_arbitrage(market1,market2,pair)
				if arbitrage_possible:
					print("Buy" + pair[0] + "-" + pair[1] +  "on market " + market1 + " for " + buy_offer(market1,pair) + " and sell on market "
						  + market2 + " for " + sell_offer(market2,pair))

def check_and_print_arbitrages():
	sleep(5000)
	print_arbitrages()