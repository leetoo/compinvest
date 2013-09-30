import sys

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import pandas as pd
import numpy as np

def marketsim(argv):
	initial_value = int(argv[0])
	order_file = argv[1]
	output_file = argv[2]
	
	orders = pd.read_csv(order_file,names=['year','month','day','symbol','action','volumn',''],header=None)
	orders['date'] = orders.apply(lambda x: dt.datetime(x[0],x[1],x[2],16), axis = 1)
	orders = orders[['date','symbol','action','volumn']]
	orders.volumn = orders.volumn.astype(int)
	orders = orders.sort()

	startday = orders.date.irow(0)
	endday = orders.date.irow(-1)
	timeofday = dt.timedelta(hours=16)
	ldt_timestamps = du.getNYSEdays(startday, endday, timeofday)

	symbols = list(set(orders.symbol))

	# Read close data
	print "Reading Data"
	dataobj = da.DataAccess('Yahoo')
	close = dataobj.get_data(ldt_timestamps, symbols, 'close', verbose=True)
	print "Finished Reading Data"

	account = close * 0
	account['cash'] = .0
	account['value'] = .0
	
	print "Start Calculating Daily Values"
	for index, order in orders.iterrows():
	    symbol = order['symbol']
	    time = order['date']
	    vol = order['volumn'] if order['action'] == "Buy" else -order['volumn']
	    price = close[symbol][time]
	    account[symbol][time] = account[symbol][time] + vol
	    account['cash'][time] = account['cash'][time] - (vol * price)

	for i in range(1, len(account.index)):
	    account.ix[i] = account.ix[i-1] + account.ix[i]
	    
	account['value'] = (account.ix[:,:-1] * close).sum(axis=1) + account['cash'] + initial_value

	account['Year'] = account.index.map(lambda x: x.year)
	account['Month'] = account.index.map(lambda x: x.month)
	account['Day'] = account.index.map(lambda x: x.day)
	
	print "Writting Daily Values to " + output_file
	account.to_csv(output_file,index=False,cols=['Year','Month','Day','value'])

if __name__ == '__main__':
	marketsim(sys.argv[1:])
