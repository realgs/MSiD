import json
import urllib.request as req
from time import sleep

names = ['BTC-BLOCK', 'BTC-BTS', 'BTC-XRP']


def get_offers(url_request):
    with req.urlopen(url_request) as url:
        answer = json.loads(url.read().decode())
        return answer


def print_offers(name, answer, currency, amount=5):
    wanted_offers_counter = 0
    current_offer = 0
    offers_sum = 0
    print(name, end='  ')
    print(currency.lower(), 'offers: ')
    while wanted_offers_counter != amount and current_offer != len(answer["result"]):
        if answer['result'][current_offer]['OrderType'] == currency.upper():
            offer = answer['result'][current_offer]['Price']
            offers_sum += offer
            print('\tPrice:', str(offer), '\tQuantity: ',
                  str(answer['result'][current_offer]['Quantity']))
            wanted_offers_counter += 1
        current_offer += 1
    return offers_sum, amount


def get_diff(buy, sell):
    return (1 - (sell - buy) / buy) * 100


def get_average(offers_sum, amount):
    return offers_sum / amount


def print_diff(name, buy, sell):
    result = get_diff(buy, sell)
    print("Difference between buy's and sell's offers for ", name, ' is: ', result, '%', sep='', end='\n\n')


def offers_list():
    for name in names:
        request = 'https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=' + name
        answer = get_offers(request)
        (buy_sum, buy_amount) = print_offers(name, answer, "BUY")
        (sell_sum, sell_amount) = print_offers(name, answer, "SELL")
        print_diff(name, get_average(buy_sum, buy_amount), get_average(sell_sum, sell_amount))


def loop():
    while True:
        offers_list()
        sleep(5)


if __name__ == '__main__':
    loop()
