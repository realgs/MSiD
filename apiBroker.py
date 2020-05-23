import requests


def get_all_data(trading_pair):
    (fst, snd) = trading_pair.split("-")
    url = f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={fst}&tsym={snd}&allData=true"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise ConnectionError('Error during fetching the data, Error code: {}'.format(resp.status_code))
    else:
        return resp.json()

if __name__ == '__main__':
    print(get_all_data("LTC-USD"))