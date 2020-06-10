import json
import time
import requests
import string
from operator import itemgetter

market_names = ['bitstamp.net','cex.io','bitbay.net','bittrex.com']

trade_pairs = ["BTCPLN","BTCUSD","ETHEUR","ETHBTC"]

fees = {'bitstamp.net': 0.005,'cex.io': 0.0025, 'bitbay.net': 0.0043,'bittrex.com':0.002}

		#bid to kupno, ask to sprzedaz pierwszej z walut w parze
def accept_bid(wallet, trade_pair, rate, ammount, fee):
    wallet[trade_pair[3:]] = wallet[trade_pair[3:]] - (ammount * 1 / rate)
    wallet[trade_pair[:3]] = wallet[trade_pair[:3]] + (ammount - ammount * fee)

def accept_ask(wallet, trade_pair, rate, ammount, fee):
    wallet[trade_pair[3:]] = wallet[trade_pair[3:]] + (ammount * rate - ammount * rate * fee)
    wallet[trade_pair[:3]] = wallet[trade_pair[:3]] - ammount


				#operation_name np. "ticker" albo "orderbook" - zwraca odpowiedni slownik otrzymany od API
def get_resources(operation_name, market_name, trade_pair):

    url = ""
   
    if market_name == 'bitbay.net':
        url =  'https://bitbay.net/API/Public/' + trade_pair + '/' + operation_name + '.json'
 
    if market_name == 'bittrex.com':
        url = 'https://api.bittrex.com/api/v1.1/public/get' + operation_name + '?market=' + trade_pair[:3]+ '-' + trade_pair[3:] 
        if operation_name == "orderbook":
            url = url + "&type=both"

    if market_name == 'bitstamp.net':
        url =  'https://www.bitstamp.net/api/v2/'
        if operation_name == "orderbook":
            url = url + "order_book"
        else:
            url = url + operation_name
        url = url + '/' + trade_pair[:3].lower() + trade_pair[3:].lower() + '/'

    if market_name == 'cex.io':
        url = 'https://cex.io/api/'
        if operation_name == "orderbook":
            url = url + "order_book"
        else:
            url = url + operation_name
        url = url +'/' + trade_pair[:3]+ "/" + trade_pair[3:]
    if url == "":
        print("URL failed")
        return {} 
    
    try:
        recieved_dict = json.loads(str(requests.get(url).json()).replace('\'', '\"'))
    except ValueError as e:
        return {}
    #print(str(recieved_dict))
    return recieved_dict


def best_offers(market, trade_pair):
    resource_dict = get_resources("ticker",market,trade_pair)
    if 'bid' not in resource_dict.keys():
        return {}
    amounts_pair = ammounts(market, trade_pair)
    return{"ask":resource_dict['ask'],"ask_amount":amounts_pair[0],"bid":resource_dict['bid'],"bid_amount":amounts_pair[1]}

def sort_offers(list_to_sort,reverseOrder=False):
    sorted_list = sorted(list_to_sort,key=itemgetter(0),reverse=reverseOrder)
    return sorted_list
    

def ammounts(market, trade_pair):	#Zwraca pare - (ilosc w najlepszym asku,ilosc w najlepszym bidzie)

    resource_dict = get_resources("orderbook",market, trade_pair)
    if 'asks' not in resource_dict.keys():
        return (-1,-1)
    sorted_asks = sort_offers(resource_dict['asks'])
    sorted_bids = sort_offers(resource_dict['bids'],reverseOrder=True)        
    return (sorted_asks[0][1],sorted_bids[0][1])

			
def arbitrage(market1, market2, trade_pair):    #zwraca trojke(x,y,z, ilosc) x -> -1 jesli 
								#niemozliwy arbitraz oraz 1 lub 2 mowiace
    market1_values = best_offers(market1, trade_pair)	#	w ktora strone zadziala arbitraz (gdzie kupic)
    market2_values = best_offers(market2, trade_pair)	#y i z to odpowiednio ceny kupna i sprzedazy
    if market1_values == {} or market2_values == {}:		# ilosc to ilosc waluty jaka mozna zamienic
        return (-1,0,0,0)
    fee1 = fees[market1]
    fee2 = fees[market2]
#    print(str(market1_values['bid']))
    sell1 = float(market1_values['bid'])-float(market1_values['bid'])*fee1 
    sell2 = float(market2_values['bid'])-float(market2_values['bid'])*fee2 
    buy1 = float(market1_values['ask'])+float(market1_values['ask'])*fee1
    buy2 = float(market2_values['ask'])+float(market2_values['ask'])*fee2
    if buy1 < sell2:
        return (1,buy1,sell2,min(float(market1_values['bid_amount']),float(market2_values['ask_amount'])))
    if buy2 < sell1:
        return (2,buy2,sell1,min(float(market1_values['ask_amount']),float(market2_values['bid_amount'])))
    return (-1,0,0,0)


def print_arbitrage(arbitrage_tuple, market1, market2, pair):
    if arbitrage_tuple[0] == 1:
        source_market = market1
        destination_market = market2
    else:
        source_market = market2
        destination_market = market1
    print("Arbitrage possible with fees included! Buy on market " + source_market + " " + str(arbitrage_tuple[3]) + " of " + str(pair[:3]) + " with ")
    print(pair[3:] + " with price " + str(arbitrage_tuple[1]) + " and sell on market " + destination_market + " with price " + str(arbitrage_tuple[2]))

def run_arbitrage_checker():
    while True:
        for x in range(len(market_names)):
            for y in range(x+1,len(market_names)):
                for pair in trade_pairs:
                    arb = arbitrage(market_names[x],market_names[y],pair)
                    if arb[0] != -1:
                        print_arbitrage(arb,market_names[x],market_names[y],pair)
        time.sleep(0.5)    



# Z4

#Najpierw znalezc pare z duzymi odchyleniami
#Dzialac to bedzie na tej zasadzie ze liczy srednia i liczy laczne odchylenia od tej sredniej 
#
#Po znalezieniu takiej pary
#Pozniej, jezeli od 10 iteracji lub wiecej cena best aska spada to czekamy az zacznie rosnac (minimum lokalne) i kupujemy
#Jednoczesnie, jezeli od 10 iteracji lub wiecej cena best bida rosnie to czekamy az zacznie spadac (maximum lokalne) i sprzedajemy
#Jednoczesnie drugim wymogiem jest ze wartosci musza byc odpowiednoi minimum i maximum na przedziale ostatnich 1000 ofert 

def find_pair_with_biggest_deviation(market,iterations):
    		#Algorytm dziala w obrebie 100 iteracji
    asks = {}
    bids = {}
    for pair in trade_pairs:
        asks[pair] = []
        bids[pair] = []
    for i in range(iterations): 
        for pair in trade_pairs:
            resources_dict = best_offers(market,pair)
            asks[pair].append(resources_dict['ask'])
            bids[pair].append(resources_dict['bid'])
        time.sleep(0.1)
    best_pair = trade_pairs[0]
    biggest_deviation_sum = 0.0
    for pair in trade_pairs:
        average_ask = sum(asks[pair]) / len(asks[pair])
        average_bid= sum(bids[pair]) / len(bids[pair])
        sum_of_deviations_asks = 0.0
        sum_of_deviations_bids = 0.0
        for ask in asks[pair]:
            sum_of_deviations_asks += abs(ask - average_ask)
        for bid in bids[pair]:
            sum_of_deviations_bids += abs(bid - average_bid)
        if sum_of_deviations_asks + sum_of_deviations_bids > biggest_deviation_sum:
            biggest_deviation_sum = sum_of_deviations_asks + sum_of_deviations_bids
            best_pair = pair
    return pair

											#Step - czas w sekundach miedzy iteracjami
def run_speculation_agent(wallet, market,iterations_to_specify_deviated_pair,iterations_to_start,step):
    pair = find_pair_with_biggest_deviation(market,iterations_to_specify_deviated_pair)
    print("Chosen pair with biggest deviation! The chosen pair is " + pair)
    asks = []
    bids = []
    for step in range(iterations_to_start):
        resources_dict = best_offers(market,pair)
        asks.append(resources_dict['ask'])
        bids.append(resources_dict['bid'])
    last_iteration_ask = asks[len(asks)-1] 
    last_iteration_bid = bids[len(bids)-1]
    times_ask_is_lowering = 0
    times_bid_is_increasing = 0
    while True:
        resources_dict = best_offers(market,pair)
        ask = resources_dict['ask']
        bid = resources_dict['bid']
        asks.append(ask)
        bids.append(bid)
        
        if times_ask_is_lowering > 10:
            if ask < last_iteration_ask and ask == min(asks[-1000:]):
                accept_ask(wallet, pair, ask, min(wallet[pair[:3]],resources_dict['ask_amount']) , fees[market])
                print("Minimum of asks found! Decision made - accepting ask for price: " + ask + " ammount possible to buy: " + min(wallet[pair[:3]],resources_dict['ask_ammount']))
                print("Wallet state after transaction: " + str(wallet))

        if times_bid_is_increasing > 10:
            if bid > last_iteration_bid and bid == max(bids[-1000:]):
                accept_bid(wallet, pair, bid, min(wallet[pair[3:]],resources_dict['bid_amount']) , fees[market])

                print("Maximum of bids found! Decision made - accepting bid for price: " + bid + " ammount possible to buy: " + min(wallet[pair[3:]],resources_dict['bid_ammount']))
                print("Wallet state after transaction: " + str(wallet))
        if ask < last_iteration_ask:
            times_ask_is_lowering += 1
        else:
            times_ask_is_lowering = 0        

        if bid > last_iteration_bid:
            times_bid_is_increasing += 1
        else:
            times_bid_is_increasing = 0
        
        last_iteration_ask = ask
        last_iteration_bid = bid

        time.sleep(step)

def main():
    wallet = {"ETH": 100.0, "USD": 100.0, "LTC": 100.0, "BTC": 100.0, "EUR": 100.0,"PLN" : 100.0}
#    run_arbitrage_checker() 
    run_speculation_agent(wallet,"bitbay.net",10,10,0.1)

main()