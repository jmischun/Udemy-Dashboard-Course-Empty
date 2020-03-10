# Imports
import os
import datetime as dt
import pandas as pd
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries


def bbands_dataframe(stock=stock):
    # Set variables
    av_key = os.environ['ALPHAVANTAGE_API_KEY']
    period = 60

    ts = TimeSeries(key=av_key, output_format='pandas')
    ti = TechIndicators(key=key, output_format='pandas')

    data_ts = ts.get_intraday(stock.upper(), interval='1min', outputsize='full')
    data_ti, meta_data_ti = ti.get_bbands(symbol=stock.upper(), interval='1min',
                                          time_period=period, series_type='close')

    # Structure data
    price_df = data_ts[0][period::]
    stock_data_df = pd.merge(price_df, data_ti, on='date')

    # Trade parameters
    low = []
    for l in stock_data_df['3. low']:
        low.append(float(l))

    high = []
    for h in stock_data_df['2. high']:
        high.append(float(h))

    bb_low = []
    for bl in stock_data_df['Real Lower Band']:
        bb_low.append(float(bl))

    bb_high = []
    for bh in stock_data_df['Real Upper Band']:
        bb_high.append(float(bh))

    # Trade Rules
    # -----------

    # Buy signal
    buy = []
    buy_index = []

    for bl, p, idx in zip(bb_low, low, stock_data_df.index[::-1]):
        if p < bl:
            if not buy_index:
                buy.append(p)
                buy_index.append(idx)
            else:
                index_need_to_beat = buy_index[-1] + dt.timedelta(minutes=30)
                if idx > index_need_to_beat:
                    buy.append(p)
                    buy_index.append(idx)

    # Sell signal
    sell = []
    sell_index = []

    for bh, p, idx in zip(bb_high, high, stock_data_df.index[::-1]):
        if p < bh:
            if not sell_index:
                sell.append(p)
                sell_index.append(idx)
            else:
                index_need_to_beat = sell_index[-1] + dt.timedelta(minutes=30)
                if idx > index_need_to_beat:
                    sell.append(p)
                    sell_index.append(idx)

    buy_positions = 0
    profit = 0
    stocks = 0
    buy_point = 0
    sell_point = 0

    while buy_point != len(buy):
        if buy_index[buy_point] < sell_index[sell_point]:
            buy_positions += round(float(buy[buy_point]))
            print(f'buy position = {buy[buy_point]} total positions = {round(buy_positions, 2)} at sell index = {sell_index[sell_point]}')
            buy_point += 1
            stocks += 1
        else:
            print(f'sold at {sell[sell_point]}')
            profit += buy_positions - (float(sell[sell_point]) * stocks)
            profit = round(profit, 2)
            print(f'profit = {profit}')
            print('')
            buy_positions = 0
            stocks = 0
            sell_point += 1
    else:
        pass

    return print(f'${profit}')


bbands_dataframe()
