import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
import csv

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""

def find_events(ls_symbols, d_data):
    ''' Finding the event dataframe '''
    df_aclose = d_data['actual_close']
    ts_market = df_aclose['SPY']

    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_aclose)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_aclose.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamps
            f_symprice_today = df_aclose[s_sym].ix[ldt_timestamps[i]]
	    f_symprice_yest = df_aclose[s_sym].ix[ldt_timestamps[i - 1]]
		
	    # Event is found if the symbol down from above $5 to below $5
            if f_symprice_today < 8.0 and f_symprice_yest >= 8.0:
	        df_events[s_sym].ix[ldt_timestamps[i]] = 1
    
    return df_events

def generate_orders(df_events,out_file):
    out = csv.writer(open(out_file,"w"), delimiter=',')
    ldt_timestamps = df_events.index
    print "Generating Orders From Events to " + out_file
    for s_sym in df_events.columns:
        for i in range(0, len(ldt_timestamps)):
            if df_events[s_sym].ix[ldt_timestamps[i]] == 1:
		buy_date = ldt_timestamps[i]
		sell_date = ldt_timestamps[i+5]
                out.writerow((buy_date.year, buy_date.month, buy_date.day, s_sym, "Buy", 100,''))
		out.writerow((sell_date.year, sell_date.month, sell_date.day, s_sym, "Sell", 100,''))
    return

if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')

    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_events = find_events(ls_symbols, d_data)
    generate_orders(df_events, "orders.csv")
