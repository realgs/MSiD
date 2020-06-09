from json import JSONDecodeError
import requests

API_NAMES = ['bittrex', 'bitbay', 'cex']


def get_answer(url):
    try:
        request = requests.get(url)
        answer = request.json()
        return answer
    except requests.exceptions.ConnectionError:
        print('No Internet connection. Check your network and try again later.')
        return None


def get_orderbook_url(base_currency, wanted_currency, name):
    if name == 'bittrex':
        return 'https://api.bittrex.com/api/v1.1/public/getorderbook?market=' + base_currency.upper() + '-' + \
               wanted_currency.upper() + "&type=both"
    if name == 'bitbay':
        return 'https://bitbay.net/API/Public/' + wanted_currency.upper() + base_currency.upper() + '/orderbook.json'
    if name == 'bitstamp':
        return 'https://www.bitstamp.net/api/v2/order_book/' + base_currency.lower() + wanted_currency.lower() + '/'
    if name == 'cex':
        return f'https://cex.io/api/order_book/{base_currency.upper()}/{wanted_currency.upper()}'


def get_orderbook(base_currency, wanted_currency, name):
    answer = get_answer(get_orderbook_url(base_currency, wanted_currency, name))
    buy_offers = []

    try:
        if name == 'bittrex':
            for bid in answer['result']['buy']:
                buy_offers.append((bid['Quantity'], bid['Rate']))
        if name == 'bitbay' or name == 'cex':
            for bid in answer['bids']:
                buy_offers.append((bid[1], bid[0]))
    except TypeError:
        return []
    except KeyError:
        return []
    return buy_offers


def check_availability_in_api(base_currency, wanted_currency):
    if base_currency == wanted_currency:
        return True
    answer = get_answer(get_orderbook_url(base_currency, wanted_currency, 'bittrex'))
    if answer["success"]:
        return True

    try:
        for i in range(1, len(API_NAMES)):
            answer = get_answer(get_orderbook_url(base_currency, wanted_currency, API_NAMES[i]))
            if len(answer['bids']) > 0:
                return True
    except JSONDecodeError:
        pass
    except KeyError:
        pass

    return False
