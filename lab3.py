import json
import urllib.request as req

names = ['BTC-BLOCK', 'BTC-BTS', 'BTC-XRP']


def get_offers(url_request):
    with req.urlopen(url_request) as url:
        answer = json.loads(url.read().decode())
        return answer


def print_offers(name, answer, type, amount=5):
    wanted_offers_counter = 0
    current_offer = 0
    print(name, end='  ')
    print(type.lower(), 'offers: ')
    while wanted_offers_counter != amount and current_offer != len(answer["result"]):
        if answer['result'][current_offer]['OrderType'] == type.upper():
            print('\tPrice:', str(answer['result'][current_offer]['Price']), '\tQuantity: ',
                  str(answer['result'][current_offer]['Quantity']))
            wanted_offers_counter += 1
        current_offer += 1


def offers_list():
    for name in names:
        request = 'https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=' + name
        answer = get_offers(request)
        print_offers(name, answer, "BUY")
        print_offers(name, answer, "SELL")


if __name__ == '__main__':
    offers_list()
