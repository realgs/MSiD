import requests
import time
import datetime
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import random 


def growthOrLoss(probability):
    rand = random.uniform(0,1)
    if rand <= probability:
        return 1
    else:
        return -1

def simulate(iterations, x, reg):
    sim_result = []
    for i in range(0, iterations-1):
        sim_day = []
        y = reg.predict(x)
        y = y.tolist()
        x = x.tolist()
        x = x[0]
        sim_day.append(abs(y[0][0]))
        sim_day.append(abs(y[0][1]))
        sim_day.append(growthOrLoss(y[0][2])*abs(y[0][0])*x[2]+x[2])
        sim_day.append(growthOrLoss(y[0][3])*abs(y[0][1])*x[3]+x[3])
        sim_day.append(sim_day[2]/sim_day[3])
        x = sim_day
        x = np.matrix(x)
        sim_result.append(sim_day)
    return sim_result


def start(dateFrom,dateTo):
    df = time.mktime(datetime.datetime.strptime(dateFrom, "%d/%m/%Y").timetuple())
    dt = time.mktime(datetime.datetime.strptime(dateTo, "%d/%m/%Y").timetuple())
    parameters = {"pair": "XBTUSD", "interval": 1440, "since": df}
    response = requests.get("https://api.kraken.com/0/public/OHLC", params = parameters)
    data = response.json()
    result = data['result']['XXBTZUSD']
    dataset = []
    i = 0
    for record in result:
        if record[0] > dt:
            break
        data_day = []
        data_day.append(abs((float(record[4]) - float(record[1]))/float(record[1]))) 
        if i > 0:
            data_day.append(abs((dataset[i-1][5] - float(record[6]))/dataset[i-1][5]))
        else:
            data_day.append(0)
        if i > 0 and ((float(record[4]) - float(record[1]))/float(record[1])) > 0:
            data_day.append(1)
        else:
            data_day.append(0)
        if i > 0 and ((dataset[i-1][5] - float(record[6]))/dataset[i-1][5]) > 0:
            data_day.append(1)
        else:
            data_day.append(0)
        data_day.append(float(record[4]))
        data_day.append(float(record[6]))
        data_day.append(float(record[4])/float(record[6]))
        dataset.append(data_day)
        i = i+1

    D = np.matrix(dataset)
    D = np.squeeze(np.asarray(D))
    y = D[1:,[0,1,2,3]]
    X = D[:-1,[0,1,4,5,6]]
    print(X)
    print(y)
    regressor = LinearRegression()
    model = regressor.fit(X, y)

    X_pred = D[-1:,[0,1,4,5,6]]
    print(np.matrix(simulate(10, X_pred, model)))
    

if __name__ == "__main__":
    start("01/04/2020","01/06/2020")
    #print(random.uniform(0,1))



