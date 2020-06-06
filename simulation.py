from datetime import datetime
import requests
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA

CURRENCY_LIST = ["BTC_LTC", "BTC_ETH", "USDT_BTC"]
API_URL = "https://poloniex.com/public?command=returnChartData"
PERIOD = 14400

"""
avaible
300 = 5min
900 = 15min
1800 = 30min
7200 = 120 min = 2h
14400 = 240 min = 4h
86400 = 1440 min = 24h
"""


def downloading_historical_data(currency, date_from, date_to):
    date_from = converting_date_to_second(date_from)
    date_to = converting_date_to_second(date_to)
    trade_history = requests.get(API_URL + "&currencyPair=" + str(currency) + "&start=" + str(date_from) + "&end=" +
                                 str(date_to) + "&period=" + str(PERIOD))
    trade_history_json = trade_history.json()
    if not trade_history_json[0] == "error":
        return trade_history_json
    else:
        raise Exception


def converting_date_to_second(date):
    yyyy = int(date[0:4])
    mm = int(date[5:7])
    dd = int(date[8:10])
    h = int(date[11:13])
    minutes = int(date[14:16])
    s = int(date[17:19])
    return int(datetime.timestamp(datetime(yyyy, mm, dd, h, minutes, s)))


def converting_second_to_date(timestamp):
    date = str(datetime.fromtimestamp(timestamp))
    if PERIOD >= 86400:
        return date[0:10]
    else:
        return date


def speculation(data, currency):
    time_api = []
    exhange_rate_api = []
    for i in range(len(data)):
        time_api.append(converting_second_to_date(data[i]["date"]))
        exhange_rate_api.append(data[i]["close"])

    data_size = len(exhange_rate_api)
    for x in range(data_size):
        model = ARIMA(exhange_rate_api, order=(1, 1, 1))
        model_fit = model.fit(disp=False)
        expected_data = model_fit.predict(len(exhange_rate_api), len(exhange_rate_api), typ='levels')

        new_date = converting_second_to_date(converting_date_to_second(time_api[len(time_api) - 1]) + PERIOD)
        time_api.append(new_date)
        exhange_rate_api.append(expected_data[0])

    half_number_of_data = int(len(exhange_rate_api) / 2)
    some_date_data_from_api = time_api[0:half_number_of_data]
    some_rate_data_from_api = exhange_rate_api[0:half_number_of_data]

    some_date_data_predicted = time_api[half_number_of_data-1::]
    some_rate_data_predicted = exhange_rate_api[half_number_of_data-1::]

    plt.plot(some_date_data_from_api,
             some_rate_data_from_api)
    plt.plot(some_date_data_predicted,
             some_rate_data_predicted)
    plt.grid(True)
    plt.xlabel("Data")
    plt.ylabel("Kurs waluty")
    plt.title("Wykres kursu kryptowaluty: " + currency[:3] + "-" + currency[4:])
    plt.show()


def predict_the_future_on_the_stock_exchange(currency, date_from, date_to):
    data = downloading_historical_data(currency, date_from, date_to)
    speculation(data, currency)


def main():
    predict_the_future_on_the_stock_exchange(CURRENCY_LIST[0], "2020-05-01 00:00:00", "2020-06-01 00:00:00")


if __name__ == '__main__':
    main()
