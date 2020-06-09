import requests


def get_url_data(url):
    try:
        request = requests.get(url)
        answer = request.json()
        return answer
    except requests.exceptions.ConnectionError:
        print('No Internet connection. Check your network and try again later.')
        return None


def get_need_data(time_from, time_to, pair):
    if pair == 1:
        answer = get_url_data(f'https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start='
                              f'{time_from}&end={time_to}&period=86400')
    elif pair == 2:
        answer = get_url_data(
            f'https://poloniex.com/public?command=returnChartData&currencyPair=USDT_ETH&start={time_from}'
            f'&end={time_to}&period=86400')
    elif pair == 3:
        answer = get_url_data(
            f'https://poloniex.com/public?command=returnChartData&currencyPair=USDT_LTC&start={time_from}'
            f'&end={time_to}&period=86400')
    else:
        raise ValueError('There is no such pair.')
    return answer
