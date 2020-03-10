# Imports
import os
import datetime as dt
import pandas as pd
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import dash
import dash_html_components as html
import dash_core_components as dcc, dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

# Set stylesheets
ext_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize app
app = dash.Dash()

app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='https://codepen.io/chriddyp/pen/bWLwgP.css'
    ),
    html.Div([
        dcc.Input(id='input-box', value='', type='text', placeholder='Enter a Stock symbol'),
        dcc.Input(id='wait-time-box', value='', type='number', placeholder='Wait Time Min.'),
        dcc.Input(id='stocks-number-box', value='', type='number', placeholder='Stocks per Buy'),
        html.Button('Submit', id='button')
    ]),
    html.Div(),
    html.P('5 Calls Per Min'),
    dcc.Tabs(id='tabs', value='graph-1', children=[
        dcc.Tab(label='Bollinger Band', value='graph-1', children=[
            html.H2(id='profit-text'),
            html.Div(dcc.Graph(id='candle-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'})),
            html.Div(id='table-div')
        ]),
        dcc.Tab(label='RSI', value='graph-2', children=[
            html.Div(dcc.Graph(id='candle-graph2', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}))
        ])
    ]),
    html.Div([
        html.P('Developed by ', style={'display': 'inline', 'color': 'white'}),
        html.A('Josh Mischung', href='http://knoasis.io/'),
        html.P(' - ', style={'display': 'inline', 'color': 'white'}),
        html.A('josh@knoasis.io', href='mailto:josh@knoasis.io')
    ], className='twelve columns',
       style={'fontSize': 18, 'padding-top': 20})
])

# Set variables
av_key = os.environ['ALPHAVANTAGE_API_KEY']
period = 60
ts = TimeSeries(key=av_key, output_format='pandas')
ti = TechIndicators(key=av_key, output_format='pandas')

# Interact with data
@app.callback([Output('candle-graph', 'figure'),
               Output('candle-graph2', 'figure'),
               Output('profit-text', 'children'),
               Output('table-div', 'children')],
              [Input('button', 'n_clicks'), Input('tabs', 'value')],
              [
                  State('input-box', 'value'),
                  State('wait-time-box', 'value'),
                  State('stocks-number-box', 'value')
              ])
def update_layout(n_clicks, tab, input_value, input_wait, input_stocks):
    # Getting dataframes ready
    data_ts = ts.get_intraday(symbol=input_value.upper(), interval='1min', outputsize='full')
    data_ti, meta_data_ti = ti.get_rsi(symbol=input_value.upper(), interval='1min',
                                          time_period=period, series_type='close')
    data_ti_2, meta_data_ti_2 = ti.get_bbands(symbol=input_value.upper(), interval='1min',
                                       time_period=period, series_type='close')

    # Structure data
    price_df = data_ts[0][period::]
    rsi_df = data_ti
    bb_df = data_ti_2
    stock_data_df = pd.merge(price_df, rsi_df, on='date')
    stock_data_df = pd.merge(stock_data_df, bb_df, on='date')

    """Price data"""
    opens = []
    for o in stock_data_df['1. open']:
        opens.append(float(o))

    high = []
    for h in stock_data_df['2. high']:
        high.append(float(h))

    low = []
    for l in stock_data_df['3. low']:
        low.append(float(l))

    close = []
    for c in stock_data_df['4. close']:
        close.append(float(c))

    """Bollinger Bands Data"""
    bb_low = []
    for bl in stock_data_df['Real Lower Band']:
        bb_low.append(float(bl))

    bb_middle = []
    for bm in stock_data_df['Real Middle Band']:
        bb_middle.append(float(bm))

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
                index_need_to_beat = buy_index[-1] + dt.timedelta(minutes=input_wait)
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
                index_need_to_beat = sell_index[-1] + dt.timedelta(minutes=input_wait)
                if idx > index_need_to_beat:
                    sell.append(p)
                    sell_index.append(idx)

    buy_positions = 0
    profit = 0
    stock_buy_inc = input_stocks
    stocks = 0
    buy_point = 0
    sell_point = 0
    values_df_prep = {
        'index': [],
        'Buy Price': [],
        'Sell Price': [],
        'Profit': []
    }

    while buy_point != len(buy):
        if buy_index[buy_point] < sell_index[sell_point]:
            buy_positions += round(float(buy[buy_point] * stock_buy_inc))
            stocks += stock_buy_inc
            values_df_prep['index'].append(buy_index[buy_point])
            values_df_prep['Sell Price'].append(0)
            values_df_prep['Buy Price'].append(buy[buy_point])
            values_df_prep['Profit'].append(f'{round(profit, 2)}')
            buy_point += 1
        else:
            sell_price = round(sell[sell_point] * stocks, 2)
            profit += sell_price - buy_positions
            values_df_prep['Buy Price'].append(0)
            values_df_prep['Sell Price'].append(round(sell[sell_point] * stocks))
            values_df_prep['index'].append(sell_index[sell_point])
            values_df_prep['Profit'].append(f'{round(profit, 2)}')
            buy_positions = 0
            stocks = 0
            sell_point += 1
    else:
        pass

    profit_df = pd.DataFrame.from_dict(values_df_prep, orient='index')
    profit_df = profit_df.T

    """RSI Data"""
    rsi_offset = []
    for r, l in zip(stock_data_df['RSI'], low):
        rsi_offset.append(l - (l / r))

    # Sell scatter
    sell_rsi_value = []
    sell_rsi_time = []

    for value, time, r in zip(stock_data_df['RSI'], stock_data_df.index, rsi_offset):
        if value > 60:
            if not sell_rsi_time:
                sell_rsi_value.append(r)
                sell_rsi_time.append(time)
            else:
                index_need_to_beat = sell_rsi_time[-1] + dt.timedelta(minutes=input_wait)
                if time > index_need_to_beat:
                    sell_rsi_value.append(r)
                    sell_rsi_time.append(time)

    # Buy scatter
    buy_rsi_value = []
    buy_rsi_time = []

    for value, time, r in zip(stock_data_df['RSI'], stock_data_df.index, rsi_offset):
        if value < 35:
            if not buy_rsi_time:
                buy_rsi_value.append(r)
                sell_rsi_time.append(time)
            else:
                index_need_to_beat = buy_rsi_time[-1] + dt.timedelta(minutes=input_wait)
                if time > index_need_to_beat:
                    buy_rsi_value.append(r)
                    sell_rsi_time.append(time)

    # Bollinger Bands Graph
    band_low = go.Scatter(
        x=stock_data_df.index[::-1],
        y=bb_low,
    )
    band_middle = go.Scatter(
        x=stock_data_df.index[::-1],
        y=bb_middle,
    )
    band_high = go.Scatter(
        x=stock_data_df.index[::-1],
        y=bb_high,
    )
    buy_band = go.Scatter(
        x=buy_index,
        y=buy,
        mode='markers',
        name='Buy'
    )
    sell_band = go.Scatter(
        x=sell_index,
        y=sell,
        mode='markers',
        name='Sell'
    )

    # RSI graph
    scatter = go.Scatter(
        x=sell_rsi_time,
        y=sell_rsi_value,
        mode='markers',
        name='Sell'
    )
    scatter_buy = go.Scatter(
        x=buy_rsi_time,
        y=buy_rsi_value,
        mode='markers',
        name='Buy'
    )
    rsi = go.Scatter(
        x=stock_data_df.index[::-1],
        y=rsi_offset
    )

    # Price Action
    BuySide = go.Candlestick(
        x=stock_data_df.index,
        open=opens,
        high=high,
        low=low,
        close=close,
        increasing={'line': {'color': '#00CC94'}},
        decreasing={'line': {'color': '#F50030'}},
        name='candlestick'
    )

    data = [BuySide, rsi, scatter, scatter_buy]
    data_bb = [BuySide, band_low, band_middle, band_high, buy_band, sell_band]

    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(type="category"),
        yaxis=dict(range=[min(rsi_offset), max(high)]),
        font=dict(color='white')
    )

    layout_bb = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(type="category"),
        yaxis=dict(range=[min(bb_low), max(bb_high)]),
        font=dict(color='white')
    )

    if tab == 'graph-1':
        return {'data': data_bb, 'layout': layout_bb}, {'data': data, 'layout': layout}, f'Profit = ${round(profit, 2)}', \
        html.Div(dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in profit_df.columns],
            data=profit_df.to_dict('rows'),
            style_cell={'width': '300px', 'height': '30px', 'textAlign': 'left'}
        ))
    elif tab == 'graph-2':
        return {'data': data_bb, 'layout': layout_bb}, {'data': data, 'layout': layout}, f'Profit = ${round(profit, 2)}', \
        html.Div(dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in profit_df.columns],
            data=profit_df.to_dict('rows'),
            style_cell={'width': '300px', 'height': '30px', 'textAlign': 'left'}
        ))

if __name__ == '__main__':
    app.run_server(port=8085)