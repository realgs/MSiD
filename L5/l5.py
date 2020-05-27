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
wallet = {"ETH": 0.0, "USD": 0.0, "LTC": 0.0, "BTC": 0.0, "EUR": 0.0}

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
    #print("With fee:  Buy: " + str(buy) + " Sell: " + str(sell))
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
    #print(str((buy_ammount,sell_ammount)))
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
    wallet[target_currency] = wallet[target_currency] + (ammount * rate - ammount * rate * fee / 100.0)
    wallet[source_currency] = wallet[source_currency] - (ammount + ammount * fee / 100.0)
    print("Buy " + str(ammount) + " of " + str(target_currency) + " for " + str(source_currency) + " with rate " + str(rate))
    print("Wallet now: " + str(wallet))

def sell(source_currency, target_currency, rate, ammount, fee):
    rev_rate = 1.0 / rate
    wallet[source_currency] = wallet[source_currency] + (ammount * rev_rate - ammount * rev_rate * fee / 100.0)
    wallet[target_currency] = wallet[target_currency] - (ammount + ammount * fee / 100.0)
    print("Sell " + str(ammount) + " of " + str(target_currency) + " for " + str(source_currency) + " with rate " + str(rate))
    print("Wallet now: " + str(wallet))

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


#Moj algorytm
#Dla ustalonego marketu tworzy slownik, ktory dla kazdej pary walut zwraca pare list
#Listy te są historiami odpowiednio bid-ow i ask-ow dla danej pary w danym markecie
#Co sekunde uruchamia się pętla, ktora dodaje do historii aktualne najlepsze oferty
#Nastepnie sprawdza czy dlugosc tablic nie przekracza 1500 - wtedy usuwa 50 najstarszych wpisow
#Jezeli wpisow jest ponad 100 to algorytm moze zaczac wystawiac oferty
#Algorytm liczy jak bardzo funkcja jest "hustajaca sie" - liczy najpierw srednia wartosc funkcji
#a nastepnie dla kazdego punktu liczy odleglosc punktu od sredniej (blad)
#Wzgledne odchylenie to srednie odchylenie punktu od sredniej arytmetycznej podzielone jeszcze przez wartosc tej sredniej
#Algorytm liczy wzgledne odchylenie zarowno dla Bid-ow jak i Ask-ow a nastepnie ustala ich wspolne za pomoca
#Sredniej arytmetycznej obu odchylen
#Jezeli wzgledne odchylenie jest wystarczajaco duze, wieksze niz ustalona wartosc, ktora ustalilem przez analize rynku
#To znaczy ze rynek ten jest wystarczajaco zroznicowany i mozna na nim grac
#W takiej sytuacji sprawdzam czy wartosc, za ktora moge kupic jest minimalna wzgledem calej historii - wtedy kupuje
#lub, za ktora moge sprzedac maksymalna - wtedy sprzedaje
def analyze_market(market):
    dict = {}
    for pair in currency_pairs:
        dict[pair] = ([],[])		#Przypisanie do każdej pary walut pary pustych list
                                #Z lewej jest tablica bid-ow, z prawej ask-ow zarejestrowanych
    while True:
        time.sleep(1)
#        print(str(dict))
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
       #         print("Average deviation on market " + market + " " + str(av_deviation) + " needs to be at least 0.00025 to commit action")
                if av_deviation > 0.00025:		#Dzialam tylko jezeli funkcja ma wzgledne odchylenie powyzej tej wartosci
                                                                # (patrzy wyzej
                                                                #Wzgledne odchylenie (relative_dev_ask i bid)
                    ammounts = ammounts_of_best_offers(market, market, pair)
                    if best_offers_pair[0] == min(dict[pair][0]):	#Jesli aktualna cena, za która mozemy kupic osiagnela minimum
                        buy(pair[0],pair[1],best_offers_pair[0],ammounts[0],fees[market])
                    if best_offers_pair[1] == max(dict[pair][1]):	#Jesli aktualna cena, za która mozemy sprzedaz osiagnela maximum
                        sell(pair[0],pair[1],best_offers_pair[1],ammounts[1],fees[market])

#print("Note: algorythm of analysis needs some data first, so wait few minutes for first output.")
#analyze_market("bitbay.net")
#To check arbitrages algorythm uncomment below line, and comment above one
#run_arbitrages()

#L5

def last_transaction(market, currency_pair):
    if currency_pair[0] == currency_pair[1]:
        return 1.0              #Jezeli chcemy konwersji np z BTC do BTC to nie liczymy tylko dajemy ze 1.0 mnoznik
    url = ticker_url(market,currency_pair)
    req = requests.get(url)
    if str(req) != "<Response [200]>":
        return None         #Jezeli nie mozna polaczyc sie z danym url to zwroc None
    jsonText = req.json()
    repairedJson = str(jsonText).replace("\'", "\"")

    #		print(repairedJson)
    dict = json.loads(repairedJson)
    #print(float(dict['last']))
    if 'last' in dict.keys():
        return float(dict['last'])
    return -1.0              #Jezeli wystapil inny blad (np. dostaniemy poprawna odpowiedz od API, ze nie ma takiej
                                        # pary walut w systemie, to zwracamy -1.0

                #Waluty musza byc zapisane w pliku wielkimi literami
def get_json_from_file(filename):

                        #Funkcja odczytuje dane z pliku JSON o podanej ścieżce w argumencie wywołania funkcji
def summarize_wallet(market, filename):         #Zwraca pare (Waluta, Wartosc), ktora mowi jaka jest waluta w ktorej podajew
    sum = 0.0                                       #I ile posiadamy w tej walucie pieniedzy
    jsonText = get_json_from_file(filename)
    repairedJson = str(jsonText).replace("\'", "\"")
    dict = json.loads(repairedJson)
    if "base_currency" not in dict.keys():
        print("Error - no base currency specified in JSON file!")
        return None
    base_curr = dict['base_currency']
    dict.pop(base_curr)
                        #Dla kazdej waluty w jakiej mamy srodki (key = waluta)
    for key in dict.keys():
        pair = (base_curr, key)
        last_trans = last_transaction(market, key)
        if last_trans == None:
            print("Error - can't connect to API or no pair " + str(pair) + " in market " + market)
        elif last_trans == -1.0:
            print("No pair " + str(pair) + "in market" + market)
        else:
            sum = sum + dict[key] * last_transaction(market, (base_curr, key))
    return (base_curr, sum)

    repairedJson = str(jsonText).replace("\'", "\"")


#Pobrac liste walut w jakich mamy z pliku w formacie JSON
#Na samym poczatku jest pod kluczem base_currency waluta do ktorej chcemy przeliczac
#Sprawdzic tylko w jednym wybranym markecie wszystkie waluty
#Wszystko na biezaco przeliczac do wybranej wczesniej waluty
#Jezeli nie bedzie takiej pary walut w markecie to wyswietlamy wiadomosc odpowiednia (req != 200 OR "last" not in dict.keys)
#