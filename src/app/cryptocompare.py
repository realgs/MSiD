from app.utils import get_json_data

def get_data(timestamp_from, timestamp_to, market_1, market_2):
    url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={market_1}&tsym={market_2}&allData=true'
    data = get_json_data(url)['Data']['Data']
    filtered_data = [d for d in data if d['time'] >= timestamp_from and d['time'] <= timestamp_to]
    return filtered_data
