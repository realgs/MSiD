# StockApp

External libraries used: gson, apache.math3, kotlinx-coroutines, knowm.xchart, xerial:sqlite-jdbc

Method `ex1_3()` and `ex4RealTime()` implement task functionalities. Method `simulationEx4()` uses real data gathered in past 
and executes `ex4()` code in "fast-forward" manner, sleeping for a while each time decision agent makes some decision.

Data is stored in an SQLite database, in file called `buySell.db`

`Ex4()` code has a visual representation.

### How does speculation algorithm work:

App learns what is an expected value (mean) of price through time. It won't make any decision if it was collecting data 
for less than an hour (720 iterations). Later it will take into account only last one-hour values (older data is dropped).

The transaction might be made only if value is abnormal, which means it is unusually big or unusually small. In other words
if it exceeds standard deviation of value in right direction (rising for selling and falling for buying).

When it exceeds that value, app starts gathering statistics about "extreme values" - values exceeding standard deviation.

Even thought value is abnormally high or low, it doesn't mean they can't be even bigger/smaller. Algorithm will make a decision
to execute a transaction only when value starts to dangerously fall/rise.

To do that it gathers information about extreme values in much smaller range of last 3 minutes (36 iterations). Works similarly
to all data decision maker, but this time a standard deviation is threshold that when crossed (while still being outside
standard deviation of 1-hour data) determines a decision to buy or sell.
