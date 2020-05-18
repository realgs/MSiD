#Najpierw zaimplementuje algorytm bioracy dane, ktorych pobieranie zaimplementuje
#pozniej

#Bedzie 16 sprawdzen czy oferta sprzedazy jest mniejsza jak oferta kupna

#Przy kalkulacjach brac pod uwage prowizje

import requests
import string
import json
import time

markets = ['bitbay.net','bittrex.com','bitstamp.net','cex.io']

currency_pairs = [("ETH","USD"),("LTC","BTC"),("ETH","EUR"),("ETH","BTC")]

	#Portfel sprawdza dla kazdej pary walut osobno
wallet = {("ETH","USD"): 0.0,("LTC","BTC"): 0.0,("ETH","EUR"): 0.0,("ETH","BTC"): 0.0}

#Fees in percent values
fees = {'bitbay.net': 0.43,'bittrex.com': 0.2,'bitstamp.net': 0.5,'cex.io': 0.25}

def orderbook_url(market, currency_pair):
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

def ticker_url(market, currency_pair):
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

def bid_ask_pair(market, pair):
	url = ticker_url(market,pair)
	req = requests.get(url)
#	print(req)
	jsonText = req.json()
	repairedJson = str(jsonText).replace("\'", "\"")
	if "message" not in repairedJson:			#jesli pojawia sie "message" to znaczy ze cos sie nie powiodlo
#		print(repairedJson)
		dict = json.loads(repairedJson)
		bid = None
		ask = None
		if 'bid' in dict.keys():
			bid = dict['bid']
		if 'ask' in dict.keys():
			ask = dict['ask']
		return (float(bid),float(ask))
	return (None, None)

def sell_offer(market, pair):
	pair = bid_ask_pair(market, pair)
	return pair[0]

def buy_offer(market, pair):
	pair = bid_ask_pair(market, pair)
	return pair[1]

							#Sprawdza tylko czy mozna sprzedac na pierwszym i kupic na drugim, nie na odwrot
def check_arbitrage(market1, market2, pair):
	sell = sell_offer(market1,pair)	#Sprzedac moge JA		- czyli jest to czyjas chec KUPNA ode mnie
	buy = buy_offer(market2,pair)	#Kupic moge JA
#	print("Without fee:  Buy: " + str(buy) + " Sell: " + str(sell))
	if sell == None or buy == None:
		return False
	fee = fees[market2]
	buy = buy + buy * (fee/100.0)
	fee = fees[market1]
	sell = sell - sell * (fee/100.0)
#	print("With fee:  Buy: " + str(buy) + " Sell: " + str(sell))
	if buy < sell:
		return True
	return False
								#w market2 KUPUJEMY w market1 SPRZEDAJEMY
def ammount_of_arbitrage(market1, market2, pair):
	url = orderbook_url(market2, pair)
	req = requests.get(url)
	#	print(req)
	jsonText = req.json()
	repairedJson = str(jsonText).replace("\'", "\"")
	buy_ammount = 0.0
	sell_ammount = 0.0
	if "message" not in repairedJson:
		#		print(repairedJson)
		dict = json.loads(repairedJson)
		asks_ammount_pairs = None
		buy_ammout_pairs = None
		if 'asks' in dict.keys():
			asks_ammount_pairs = dict['asks']
			min_buy = asks_ammount_pairs[0][0]
			buy_ammount = asks_ammount_pairs[0][1]
			for pair in asks_ammount_pairs:
				if pair[0] < min_buy:
					min_buy = pair[0]
					buy_ammount = pair[1]
		if 'bids' in dict.keys():
			bids_ammount_pairs = dict['bids']
			max_sell = bids_ammount_pairs[0][0]
			sell_ammount = bids_ammount_pairs[0][1]
			for pair in bids_ammount_pairs:
				if pair[0] > max_sell:
					max_sell = pair[0]
					sell_ammount = pair[1]
	return min(buy_ammount,sell_ammount)


def loop_arbitrages():
	for market1 in markets:
		for market2 in markets:
			for pair in currency_pairs:
				arbitrage_possible = check_arbitrage(market1,market2,pair)
				if arbitrage_possible:
					print("Arbitrage!")
					ammount = ammount_of_arbitrage(market1,market2,pair)
					wallet[pair] = wallet[pair] + ammount *(sell_offer(market1,pair) - buy_offer(market2,pair))
					print("Buy " + str(ammount) + " " + pair[0] + "-" + pair[1] +  " on market " + market1 + " for " + str(buy_offer(market2,pair)) + " and sell on market "
						  + market2 + " for " + str(sell_offer(market1,pair)) + " (Including fees)")
					print("Wallet after operation: " + str(wallet))

def run_arbitrages():
	while True:
		time.sleep(1)
		loop_arbitrages()

run_arbitrages()
