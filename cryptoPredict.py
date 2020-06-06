import requests
import time
import datetime
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import random 
import matplotlib.pyplot as plt


def growthOrLoss(probability):
    rand = random.uniform(0,1)
    if rand <= probability:
        return 1
    else:
        return -1

def simulate(iterations, x, reg, dt):
    sim_result = []
    for i in range(0, iterations):
        sim_day = []
        y = reg.predict(x)
        y = y.tolist()
        x = x.tolist()
        x = x[0]
        sim_day.append(1)
        sim_day.append(abs(y[0][0]))
        sim_day.append(abs(y[0][1]))
        sim_day.append(growthOrLoss(y[0][2])*abs(y[0][0])*x[3]+x[3])
        sim_day.append(growthOrLoss(y[0][3])*abs(y[0][1])*x[4]+x[4])
        sim_day.append(sim_day[2]/sim_day[3])
        x = sim_day
        x = np.matrix(x)
        sim_day.append(dt)
        dt += 86400
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
    x_axis = []
    y_axis = []
    i = 0
    for record in result:
        if record[0] > dt:
            break
        data_day = []
        x_axis.append(record[0])
        y_axis.append(float(record[4]))
        data_day.append(1)
        data_day.append(abs((float(record[4]) - float(record[1]))/float(record[1]))) 
        if i > 0:
            data_day.append(abs((dataset[i-1][6] - float(record[6]))/dataset[i-1][6]))
        else:
            data_day.append(0)
        if i > 0 and ((float(record[4]) - float(record[1]))/float(record[1])) > 0:
            data_day.append(1)
        else:
            data_day.append(0)
        if i > 0 and ((dataset[i-1][6] - float(record[6]))/dataset[i-1][6]) > 0:
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
    y = D[1:,[1,2,3,4]]
    X = D[:-1,[0,1,2,5,6,7]]
    regressor = LinearRegression()
    model = regressor.fit(X, y)

    X_pred = D[-1:,[0,1,2,5,6,7]]
    single_simulation = np.matrix(simulate(int((dt-df)/86400), X_pred, model, dt))
    #print(single_simulation)
    """
    multi_simulation = []
    for i in range (0,100):
        multi_simulation.append(np.matrix(simulate(int((dt-df)/86400), X_pred, model)))
        print(i)
    print("Done")
    """
    second_x_axis = single_simulation[:,-1:]
    second_x_axis = second_x_axis.tolist()
    single_simulation = single_simulation[:,[2]]
    single_simulation = single_simulation.tolist()
    plt.plot(second_x_axis[0], single_simulation[0])

    plt.plot(x_axis, y_axis)
    plt.show()

if __name__ == "__main__":
    start("01/02/2020","01/06/2020")
    #print(random.uniform(0,1))