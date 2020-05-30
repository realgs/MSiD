import apiBroker
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def draw(data, title):

    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    dataset = pd.DataFrame(data)
    dataset['time'] = pd.to_datetime(dataset['time'], unit='s')
    ax1 = dataset.plot(kind='line' , x='time', y='open', title=title, ax=ax1)
    ax1.set_xlabel("time")
    ax1.set_ylabel("price")
    ax2 = dataset.plot(kind="bar", x='time', y='volumefrom', stacked=True, ax=ax2)
    ax2.set_xlabel("time")
    ax2.set_ylabel("volume")

    plt.show()


if __name__ == '__main__':
    draw(apiBroker.get_data("BTC-USD", 1589328000, 1590192000), title="BTC-USD")