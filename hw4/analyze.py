import sys

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import pandas as pd
import numpy as np

def simulate(daily_price):
	
	na_price_norm = daily_price / daily_price[0]
	na_daily_rets = na_price_norm[1:] / na_price_norm[:-1] - 1
	na_daily_rets = np.append([.0], na_daily_rets)
	
	k = np.sqrt(252)
	std_daily_ret = na_daily_rets.std()
	avg_daily_ret = na_daily_rets.mean()
	sharp_ratio = k * avg_daily_ret / std_daily_ret

	return std_daily_ret, avg_daily_ret, sharp_ratio, na_price_norm[-1]

def read_value_file(value_file):
	values = pd.read_csv(value_file)
	return values

def benchmark(symbol,start_date,end_date):
	ldt_timestamps = du.getNYSEdays(start_date, end_date, dt.timedelta(hours=16))
	ls_keys = ['close']
	c_dataobj = da.DataAccess('Yahoo')

	ldf_data = c_dataobj.get_data(ldt_timestamps, [symbol], ls_keys)
	d_data = dict(zip(ls_keys, ldf_data))
	adj_close = d_data['close'][symbol].values
	
	return simulate(adj_close)

if __name__ == '__main__':
	value_file = sys.argv[1]
	benchmark_symbol = sys.argv[2]

	port_vals = read_value_file(value_file)
	init_val = port_vals['value'].values[0]
	start_date = dt.datetime(int(port_vals.irow(0)[0]),int(port_vals.irow(0)[1]),int(port_vals.irow(0)[2]),16)
	end_date = dt.datetime(int(port_vals.irow(-1)[0]),int(port_vals.irow(-1)[1]),int(port_vals.irow(-1)[2]),16)
	
	#The performance of portfolio and benchmark
	portfolio = simulate(port_vals['value'].values)
	benchmark = benchmark(benchmark_symbol,start_date,end_date)
	print "The final value of the portfolio using the sample file is -- " , end_date.year , "," , \
	      end_date.month , "," , end_date.day , "," , portfolio[3]*init_val , "\n"

	print "Details of the Performance of the portfolio: \n"
	
	print "Data Range : ",start_date," to ",end_date,"\n"

	print "Sharp Ratio of Fund : %.11f" % portfolio[2] 
	print "Sharp Ratio of " + benchmark_symbol + ": %.11f" % benchmark[2] + '\n'

	print "Total Return of Fund : %.11f" % portfolio[3] 
	print "Total Return of " + benchmark_symbol + ": %.11f" % benchmark[3] + '\n'

	print "Standard Deviation of Fund : %.11f" % portfolio[0] 
	print "Standard Deviation of " + benchmark_symbol + ": %.11f" % benchmark[0] + '\n'

	print "Average Daily Return of Fund : %.11f" % portfolio[1] 
	print "Average Daily Return of " + benchmark_symbol + ": %.11f" % benchmark[1]
	
