from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import yfinance as yf
 
# Create Home Page Route
app = Flask(__name__)
 
pd.set_option('mode.chained_assignment', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Initialise the data 
fast_MA = 5
slow_MA = 9
initial_wealth = '1000'
#STK = input("Enter share name : ")
stock = 'SPY'

from datetime import date, timedelta
today = date.today()
end_date = today.strftime("%Y-%m-%d")
prevdayrange = today- timedelta(days=6)
start_date = prevdayrange.strftime("%Y-%m-%d")

@app.route('/')
def bar_with_plotly():

    yf.pdr_override()
    #dwl_df = yf.download(tickers=stock, start=startdate, end=enddate, interval='1d',period='60d')
    dwl_df = yf.download(tickers=stock, period='1d', interval='15m')
    dwl_df.reset_index(inplace=True) 
    dwl_df[['Open','High','Low','Close','Adj Close']] = dwl_df[['Open','High','Low','Close','Adj Close']].round(2)

    dwl_df['fast_MA'] = dwl_df['Close'].ewm(span=fast_MA, adjust=False).mean()
    dwl_df['slow_MA'] = dwl_df['Close'].ewm(span=slow_MA, adjust=False).mean()
    dwl_df[['fast_MA','slow_MA']] = dwl_df[['fast_MA','slow_MA']].round(2)
    dwl_df['intersectionpoint'] = np.where(dwl_df['fast_MA'] > dwl_df['slow_MA'], 1.0, 0.0)
    dwl_df['crossover'] = dwl_df['intersectionpoint'].diff()
    filtered_col_df = dwl_df[['Datetime','Open','High','Low','Close','crossover']].copy()
    rslt_df = filtered_col_df[filtered_col_df['crossover'] != 0.0] 
    
    # Use render_template to pass graphJSON to html
    return rslt_df.to_html()
