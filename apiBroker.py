import requests



def get_all_data(trading_pair):
    (fst, snd) = trading_pair.split("-")
    url = f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={fst}&tsym={snd}&allData=true"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise ConnectionError('Error during fetching the data, Error code: {}'.format(resp.status_code))
    else:
        return resp.json()


def get_data(trading_pair, timestamp_from, timestamp_to):
    data = get_all_data(trading_pair)
    return filter(lambda data:  float(timestamp_from) <= float(data["time"]) <= float(timestamp_to), data["Data"]["Data"])


if __name__ == '__main__':
    data = get_data("BTC-USD", 1589328000, 1590192000)
    for record in data:
        print(record)
