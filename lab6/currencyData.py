import datetime


def generate_url(start, end='now', interval="3h", currency='btc-bitcoin'):
    if end == 'now':
        end = ''
    else:
        end = 'end=%s&' % end
    return 'https://api.coinpaprika.com/v1/tickers/%s/historical?start=%s&%slimit=5000&interval=%s' \
           % (currency, start, end, interval)


def prepare_values(data):
    dates, prices, volumes = [], [], []
    for node in data:
        formatted_date = datetime.datetime \
            .strptime(node.get('timestamp'), '%Y-%m-%dT%H:%M:%SZ')
        dates.append(formatted_date)
        prices.append(node.get('price'))
        volumes.append(node.get('volume_24h') / 10000000)
    return dates, prices, volumes


def generate_dates(first, time_step, elements):
    base = datetime.datetime.strptime(first, '%Y-%m-%d %H:%M:%S')
    dates = []
    for x in range(elements):
        dates.append(base)
        base = base + time_step
    return dates


def count_average(values, fun):
    to_return = []
    for value in values:
        to_return.append(fun(value))
    return to_return


def generate_future_values(forecaster):
    all_prices, all_volumes = [], []
    for i in range(forecaster.total):
        all_prices.append([])
        all_volumes.append([])
    for i in range(100):
        new_prices, new_volumes = forecaster.forecast()
        for j in range(len(new_prices)):
            all_prices[j].append(new_prices[j])
            all_volumes[j].append(new_volumes[j])
    return all_prices, all_volumes


def generate_stats(all_prices, all_volumes, fun):
    return count_average(all_prices, fun), count_average(all_volumes, fun)