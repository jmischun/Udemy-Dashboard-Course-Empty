# Imports
from binance.client import Client
from datetime import datetime
from pandas import DataFrame as df
from keys import binance_key, binance_secret

def binance_price():
	# APIs
	client = Client(api_key=binance_key, api_secret=binance_secret)

	# Create dataframe
	candles = client.get_klines(symbol='LTCUSDT', interval=Client.KLINE_INTERVAL_1HOUR)
	candles_df = df(candles)

	# Format time
	candles_df_date = candles_df[0]

	final_date = []

	for time in candles_df_date.unique():
		readable = datetime.fromtimestamp(int(time/1000))
		final_date.append(readable)

	# Remove columns & concat df's
	candles_df.pop(0)
	candles_df.pop(11)

	final_date_df = df(final_date)
	final_date_df.columns = ['date']

	complete_df = candles_df.join(final_date_df)
	complete_df.set_index('date', inplace=True)
	complete_df.columns = ['open', 'high', 'low', 'close', 'volume',
						'close_time', 'asset_vol', 'num_trades',
						'taker_buy_base', 'taker_buy_quote']

	return complete_df

print(binance_price())