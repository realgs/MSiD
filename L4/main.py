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

    #Portfel sprawdza dla kazdej waluty osobno
wallet2 = {"ETH": 0.0, "USD": 0.0, "LTC": 0.0, "BTC": 0.0, "EUR": 0.0}

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
            bid = float(dict['bid'])
        if 'ask' in dict.keys():
            ask = float(dict['ask'])
        return (bid,ask)
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
    return min(ammounts_of_best_offers(market1, market2, pair))

                                #w market2 KUPUJEMY w market1 SPRZEDAJEMY
def ammounts_of_best_offers(market1, market2, pair):
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
    return (buy_ammount,sell_ammount)


def loop_arbitrages():
    for market1 in markets:
        for market2 in markets:
            for pair in currency_pairs:
                arbitrage_possible = check_arbitrage(market1,market2,pair)
                if arbitrage_possible:
                    print("Arbitrage!")
                    ammount = ammount_of_arbitrage(market1,market2,pair)
                    print("Buy " + str(ammount) + " " + pair[0] + "-" + pair[1] +  " on market " + market1 + " for " + str(buy_offer(market2,pair)) + " and sell on market "
                          + market2 + " for " + str(sell_offer(market1,pair)) + " (Including fees)")
                    buy(pair[0],pair[1],buy_offer(market2,pair),ammount,fees[market2])
                    sell(pair[0],pair[1],sell_offer(market1,pair),ammount,fees[market1])

def run_arbitrages():
    while True:
        time.sleep(1)
        loop_arbitrages()

#run_arbitrages()

#Zad 4
                #Przyjalem tutaj zalozenie - ask to oferta sprzedazy tego co po prawej stronie za to co po lewej
                    #Ammount - to jest ilosc tego co po prawej do sprzedania przez kogos
                # bid to oferta zakupu tego co po prawej za to co po lewej
                # Ammount - to jest ilosc to co po lewej ktos chce sprzedac
                #Czyli ask -> dajesz lewe dostajesz prawe	(dostajesz tyle prawego co ammount) (tracisz tyle lewego do wyliczenia)
                # bid -> dajesz prawe dostajesz lewe (tracisz tyle prawego ile ammount) (dostajesz tyle co przeliczenie)
def buy(source_currency, target_currency, rate, ammount, fee):
    wallet2[target_currency] = wallet2[target_currency] + (ammount - ammount * fee / 100.0)
    wallet2[source_currency] = wallet2[source_currency] - (ammount * rate + ammount * rate * fee / 100.0)
    print("Buy " + str(ammount) + " of " + target_currency + " for " + source_currency + " with rate " + rate)
    print("Wallet now: " + wallet2)

def sell(source_currency, target_currency, rate, ammount, fee):
    rev_rate = 1.0 / rate
    wallet2[source_currency] = wallet2[source_currency] + (ammount * rev_rate - ammount * rev_rate * fee / 100.0)
    wallet2[target_currency] = wallet2[target_currency] - (ammount + ammount * fee / 100.0)
    print("Sell " + str(ammount) + " of " + target_currency + " for " + source_currency + " with rate " + rate)
    print("Wallet now: " + str(wallet2))

def count_average(arr):
    return sum(arr) / len(arr)

def sum_errors(arr):
    sum_of_errors = 0.0
    average = count_average(arr)
    for x in arr:
        sum_of_errors = sum_of_errors + abs(x - average)
    return sum_of_errors

def average_deviation(arr):
    return sum_errors(arr) / len(arr)

def analyze_market(market):
    dict = {}
    for pair in currency_pairs:
        dict[pair] = ([],[])		#Przypisanie do każdej pary walut pary pustych list
                                #Z lewej jest tablica bid-ow, z prawej ask-ow zarejestrowanych
    while True:
        time.sleep(1)
        print(str(dict))
        for pair in currency_pairs:
            best_offers_pair = bid_ask_pair(market,pair)
            dict[pair][0].append(best_offers_pair[0])
            dict[pair][1].append(best_offers_pair[1])
            if len(dict[pair][0]) > 1500:			#Jezeli tablice maja juz dlugosc ponad 1500 to usun 50 elementow ostatnich
                for x in range(50):
                    dict[pair][0].pop(0)
            if len(dict[pair][1]) > 1500:
                for x in range(50):
                    dict[pair][0].pop(0)
            if len(dict[pair][0]) > 100:			#Jezeli danych zebrano juz ponad 100 to mozna zaczac spekulacje
                average_dev_ask = average_deviation(dict[pair][1])
                average_dev_bid = average_deviation(dict[pair][0])
                relative_dev_ask = average_dev_ask / count_average(dict[pair][1])
                relative_dev_bid = average_dev_bid / count_average(dict[pair][0])
                av_deviation = (relative_dev_ask+ relative_dev_bid) / 2.0
                print(str(av_deviation))
                if av_deviation > 0.00025:		#Dzialam tylko jezeli funkcja ma wzgledne odchylenie powyzej tej wartosci
                                                                # (patrzy wyzej
                                                                #Wzgledne odchylenie (relative_dev_ask i bid)
                    ammounts = ammounts_of_best_offers(market, market, pair)
                    if best_offers_pair[0] == min(dict[pair][0]):	#Jesli aktualna cena, za która mozemy kupic osiagnela minimum
                        buy(pair[0],pair[1],best_offers_pair[0],ammounts[0],fees[market])
                    if best_offers_pair[1] == max(dict[pair][1]):	#Jesli aktualna cena, za która mozemy sprzedaz osiagnela maximum
                        sell(pair[0],pair[1],best_offers_pair[1],ammounts[1],fees[market])

analyze_market("bitbay.net")
#run_arbitrages()
