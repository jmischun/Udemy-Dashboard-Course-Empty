# Imports
import datetime as dt
import plotly.offline as py
import plotly.graph_objs as go
import pandas_datareader as web

# Set window
start = dt.datetime(2014, 1, 1)
end = dt.datetime(2018, 1, 1)

# Stock data
FB = web.DataReader('FB', 'yahoo', start, end)
TW = web.DataReader('TWTR', 'yahoo', start, end)
AAPL = web.DataReader('AAPL', 'yahoo', start, end)

# Plot stock data
trace_1 = go.Ohlc(
	x=FB.index[:],
	open=FB['Open'],
	high=FB['High'],
	low=FB['Low'],
	close=FB['Close'],
	name='FB',
	increasing=dict(line=dict(color='blue')),
	decreasing=dict(line=dict(color='red'))
)

trace_2 = go.Ohlc(
	x=FB.index[:],
	open=TW['Open'],
	high=TW['High'],
	low=TW['Low'],
	close=TW['Close'],
	name='TW',
	increasing=dict(line=dict(color='blue')),
	decreasing=dict(line=dict(color='red'))
)

trace_3 = go.Ohlc(
	x=FB.index[:],
	open=AAPL['Open'],
	high=AAPL['High'],
	low=AAPL['Low'],
	close=AAPL['Close'],
	name='AAPL',
	increasing=dict(line=dict(color='blue')),
	decreasing=dict(line=dict(color='red'))
)

data = [trace_1, trace_2, trace_3]
layout = {
	'title': 'Facebook vs Twitter vs Apple',
	'yaxis':{'title': 'Price per stock'}
}

fig = dict(data=data, layout=layout)
py.plot(fig, filename='techstocks.html')