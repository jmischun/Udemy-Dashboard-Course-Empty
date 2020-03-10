# Imports
from binance.client import Client
import plotly.offline as pyo
import plotly.graph_objs as go
import pandas as pd
from keys import binance_key, binance_secret

client = Client(api_key=binance_key, api_secret=binance_secret)