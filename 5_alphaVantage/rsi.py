# Imports
import os
import pandas as pd
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries

# Get alpha vantage key
key = os.environ['ALPHAVANTAGE_API_KEY']

# Input
stock = input('What stock do you want?: ')
print('')


def rsi_dataframe(stock=stock):
	# Set variables
	av_key = os.environ['ALPHAVANTAGE_API_KEY']
	period = 60

	ts = TimeSeries(key=av_key, output_format='pandas')
	ti = TechIndicators(key=key, output_format='pandas')

	data_ts = ts.get_intraday(stock.upper(), interval='1min', outputsize='full')
	data_ti, meta_data_ti = ti.get_rsi(symbol=stock.upper(), interval='1min',
									   time_period=period, series_type='close')

	# Structure data
	price_df = data_ts[0][period::]
	stock_data_df = pd.concat([price_df, data_ti], axis=1, sort=True)

	return print(stock_data_df)


rsi_dataframe()