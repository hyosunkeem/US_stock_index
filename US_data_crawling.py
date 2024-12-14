import pandas as pd
import yfinance as yf
'''
import pandas_datareader as pdr
'''
import numpy as np
from datetime import datetime

tickers = ['^VXN', '^VIX', '^GSPC', '^IXIC', '^DJI']
start_date = '2000-01-23'
end_date = datetime.today().strftime('%Y-%m-%d')

data = pd.DataFrame()

for ticker in tickers:
    temp_data = yf.download(ticker, start=start_date, end=end_date)
    if ticker in ['^VXN', '^VIX']:
        temp_data = temp_data[['Adj Close']].rename(columns={'Adj Close': ticker})
    else:
        temp_data['Return'] = np.log(temp_data['Adj Close'] / temp_data['Adj Close'].shift(1))
        temp_data = temp_data[['Return']].rename(columns={'Return': ticker})
    if data.empty:
        data = temp_data
    else:
        data = data.join(temp_data)

data = data.reset_index().rename(columns={
    'index': 'date',
    '^VXN': 'vxn',
    '^VIX': 'vix',
    '^GSPC': 'sp',
    '^IXIC': 'nasdaq',
    '^DJI': 'dow'
})

data.to_csv('kim_stock.csv', index=False)