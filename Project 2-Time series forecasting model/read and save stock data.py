
"""
Weiqi Zhang
Class: CS677 - Online 2 Spring  2023
Date: 03/29/2023
Homework1 Preliminary task problem2
Description of problem:
1.to download daily stock data (5-years from Jan 1, 2018 to Dec 31, 2022) for Zillow Group as a CSV file
2.computes additional fields for time (week, day, month) and prices (daily returns, 14- and 50-day moving price averages).
"""
# run this !pip install pandas_datareader
from pandas_datareader import data as web
import os
import pandas as pd
import yfinance as yf

yf.pdr_override()

def get_stock(ticker, start_date, end_date, s_window, l_window):
    try:
        df = web.get_data_yahoo(ticker, start=start_date, end=end_date)
        df['Return'] = df['Adj Close'].pct_change()
        df['Return'].fillna(0, inplace=True)
        df['Date'] = df.index
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
        df['Day'] = df['Date'].dt.day
        for col in ['Open', 'High', 'Low', 'Close', 'Adj Close']:
            df[col] = df[col].round(2)
        # df['Weekday'] = df['Date'].dt.weekday_name
        df['Weekday'] = df['Date'].dt.day_name()
        df['Week_Number'] = df['Date'].dt.strftime('%U')
        df['Year_Week'] = df['Date'].dt.strftime('%Y-%U')
        df['Short_MA'] = df['Adj Close'].rolling(
            window=s_window, min_periods=1).mean()
        df['Long_MA'] = df['Adj Close'].rolling(
            window=l_window, min_periods=1).mean()
        col_list = ['Date', 'Year', 'Month', 'Day', 'Weekday',
                    'Week_Number', 'Year_Week', 'Open',
                    'High', 'Low', 'Close', 'Volume', 'Adj Close',
                    'Return', 'Short_MA', 'Long_MA']
        num_lines = len(df)
        df = df[col_list]
        print('read ', num_lines, ' lines of data for ticker: ', ticker)
        return df
    except Exception as error:
        print(error)
        return None


here = os.path.abspath(__file__)
input_dir = os.path.abspath(os.path.join(here, os.pardir))
tickers = ['SPY','ZG']
for ticker in tickers:
    try:
        output_file = os.path.join(input_dir, ticker + '.csv')
        print("Good job, Output file path: ", output_file)
        df = get_stock(ticker, start_date='2018-01-01', end_date='2022-12-31',
                       s_window=14, l_window=50)
        df.to_csv(output_file, index=False)
        print('wrote ' + str(len(df)) + ' lines to file: ' + output_file)
    except Exception as e:
        print(e)
        print('failed to get Yahoo stock data for ticker: ', ticker)
