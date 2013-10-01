Overview
------------------------------------------------------------------------------------------
In this homework you will take the output of your Event Study work to build a more complete back testing platform. 
Specifically, you should choose an event from the ones you have experimented with in this class, assess it and 
tune it using the Event Profiler, then back test it with the simulator you created.



To Do
------------------------------------------------------------------------------------------
Part 1: Revise your event analyzer to output a series of trades based on events; Instead of putting a 1 in the event matrix, output to a file
Date, AAPL, BUY, 100
Date + 5 days, AAPL, SELL, 100
Part 2: Feed that output into your market simulator.




Experiments to Run
------------------------------------------------------------------------------------------
You should run two experiments.
Experiment 1: Use the actual close $5.00 event with the 2012 SP500 data. I expect that this strategy should make money. We will use this example to make sure everybody is getting "correct" answers. You can share your numerical results with others to make sure you're on the right track. Use the following parameters:
Starting cash: $50,000
Start date: 1 January 2008
End date: 31 December 2009
When an event occurs, buy 100 shares of the equity on that day.
Sell automatically 5 trading days later.
Experiment 2: Devise your own event and trading strategy.
For both experiments, you should:
Create a chart to illustrate the performance of your fund.
Compute the Sharpe Ratio, total return and STDDEV of daily returns.




Other Details
------------------------------------------------------------------------------------------
You have already prepared the event study and the market simulator in the previous two homeworks. And now we shall combine the two pieces together.
It is important to note that 5 days is actually 5 trading days.
For the final few events assume that you exit on the last day, so hold it less than 5 days.





Example Output
------------------------------------------------------------------------------------------
On simulating the $5 event the output is:
The final value of the portfolio using the sample file is -- 2009,12,28,54824.0

Details of the Performance of the portfolio

Data Range :  2008-01-03 16:00:00  to  2009-12-28 16:00:00

Sharpe Ratio of Fund : 0.527865227084
Sharpe Ratio of $SPX : -0.184202673931

Total Return of Fund :  1.09648
Total Return of $SPX : 0.779305674563

Standard Deviation of Fund :  0.0060854156452
Standard Deviation of $SPX : 0.022004631521

Average Daily Return of Fund :  0.000202354576186
Average Daily Return of $SPX : -0.000255334653467
