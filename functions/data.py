import os
import pandas as pd
from alpaca.trading.client import TradingClient
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from alpaca.data import StockHistoricalDataClient, StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime


# Account Setup
trading_keys = {"KEY": "PKZIQNDORZDL6TUCH7G0", "SECRET" : "ScXDbZqalWAUFWAWUuJ76Pg4j8aBg09HjPg4tfqm"}
trade_client = TradingClient(api_key=trading_keys["KEY"], secret_key=trading_keys["SECRET"], paper=True)
account = trade_client.get_account()
accountNum = account.account_number
buyingPower = account.buying_power

print("Account #: " + accountNum + "\n")
print("Buying Power: " + str(buyingPower) + "\n")

# Training Data params
mySymbol = "SPY"
timeframe = TimeFrame.Day  # 1D = Daily data
training_start_date = '2016-01-01'
training_end_date = '2020-08-01'

# Get historical training data
historical_client = StockHistoricalDataClient(trading_keys["KEY"],trading_keys["SECRET"])
request_params = StockBarsRequest(symbol_or_symbols=mySymbol,timeframe=timeframe,start=training_start_date,end=training_end_date)
training_data = historical_client.get_stock_bars(request_params=request_params).df

# Format training data
df = pd.DataFrame(data=training_data)
df.drop(columns=['open','high','low'],inplace=True)
df.reset_index(inplace=True)
df.drop(columns=['symbol'],inplace=True)
df['timestamp'] = pd.to_datetime(df["timestamp"]).dt.date
df.set_index('timestamp',inplace=True)
df.to_csv('training_data.csv')
print(training_data.tail())

# Test Data params
mySymbol = "SPY"
timeframe = TimeFrame.Day  # 1D = Daily data
test_start_date = '2022-01-01'
test_end_date = '2025-01-01'

# Get historical test data
historical_client = StockHistoricalDataClient(trading_keys["KEY"],trading_keys["SECRET"])
request_params = StockBarsRequest(symbol_or_symbols=mySymbol,timeframe=timeframe,start=test_start_date,end=test_end_date)
test_data = historical_client.get_stock_bars(request_params=request_params).df

# Format test data
df = pd.DataFrame(data=test_data)
df.drop(columns=['open','high','low'],inplace=True)
df.reset_index(inplace=True)
df.drop(columns=['symbol'],inplace=True)
df['timestamp'] = pd.to_datetime(df["timestamp"]).dt.date
df.set_index('timestamp',inplace=True)
df.to_csv('test_data.csv')
print(test_data.tail())
