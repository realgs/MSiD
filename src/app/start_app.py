from app import plot
from app.config import START_TIME, END_TIME, MARKET_1, MARKET_2
from app import simulator

if __name__ == "__main__":
    df = simulator.simulate(START_TIME, END_TIME, MARKET_1, MARKET_2)
    plot.plot(df)
