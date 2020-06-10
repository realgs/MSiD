import requests
import time
from operator import itemgetter
import json

market_names = ['bitstamp.net','cex.io','bitbay.net','bittrex.com']

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
        url = url + '/' + trade_pair[:3] + "/" + trade_pair[3:]
 
    if url == "":
        return {} 
    
    try:
        recieved_dict = json.loads(str(requests.get(url).json()).replace('\'', '\"'))
    except ValueError as e:
        return {}
    return recieved_dict

def last_price(market, trade_pair):
    resource_dict = get_resource("ticker",market, trade_pair)
    if 'last' not in resource_dict.keys():
        return -1
    return resource_dict['last']

def input_base_currency():
    ret = input("Please specify base currency: ")
    return ret

def input_wallet():
    wallet = {}
    print("Print pairs of currency and ammount, or print END to submit your wallet")
    print("Example:")
    print("BTC 0.12365")
    line = input()
    while line != "END":
        words = line.split(" ")
        currency = words[0]
        ammount = float(words[1])
        if currency not in wallet.keys():
            wallet[currency] = ammount
        else:
            wallet[currency] += ammount
        line = input()
    return wallet
    
				#zwraca wartosc waluty bazowej po przeliczeniu
def to_base_currency_trivial(wallet, market, base_currency ):   
    sum_ammount= 0.0       
    for key in wallet.keys():
        if key == base_currency:
            sum_ammount += float(wallet[key])
        else:
            price = last_price(market, key+base_currency)
            if price == -1:
                print("No market for " + key + ":" + base_currency + " found on " + market)
                print("Currency not added to total ammount")
            else:
                sum_ammount += float(wallet[key]) * price 
    return sum_ammount 


def bids_sorted(market, trade_pair):
    resource_dict = get_resources("orderbook",market, trade_pair)
#    print(str(resource_dict))
    if 'bids' not in resource_dict:
        return []
    bids = resource_dict['bids']
#    print(str(bids))
    return sorted(bids,key=itemgetter(0),reverse=True) 

def switch_market(market):
    return market_names[(market_names.index(market)+1)%len(market_names)]

def to_base_currency(wallet, market, base_currency):         
    sum_ammount = 0.0                          
    for key in wallet.keys():
        if key == base_currency:
            sum_ammount += wallet[key]
        else:
            currency_to_sell = float(wallet[key])
            bids = bids_sorted(market, (key+base_currency))
            #print(str(bids))      
            if bids == []:
                for x in range(len(market_names)-1):
                    market = switch_market(market)
                    bids = bids_sorted(market, key+base_currency)
                    if bids != []:
                        break
                if bids == []:
                    print("No market for " + key + ":" + base_currency + " found on any market known")
                    print("Currency not added to total ammount")
            if bids != []:     
                while currency_to_sell > 0:			
                    #print(str(bids))
                    next_offer = bids.pop(0)
                    print("Next offer: " + str(next_offer))
                    next_ammount = min(currency_to_sell, float(next_offer[1]))
                    currency_to_sell -= next_ammount
                    sum_ammount += next_ammount * float(next_offer[0])
    return sum_ammount

#Dodatek
		#Sprawdzanie automatyczne co 2 sekundy wartosci portfela
def to_base_currency_loop(wallet, market, base_currency):
    time.sleep(2)
    answer = to_base_currency(wallet,market, base_currency)
    print("Total: " + str(answer))

def main():
    wallet = input_wallet()
    base_currency = input_base_currency()
    answer = to_base_currency(wallet, market_names[0], base_currency)
    print("Total of " + base_currency + " after calculation = " + str(answer))  

main()
#to_base_currency
