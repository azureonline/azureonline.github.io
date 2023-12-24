# Import Required Modules
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
stocksymbols = ['SPY','QQQ','IWM','DIA','SMH']


from datetime import date, timedelta
today = date.today()
end_date = today.strftime("%Y-%m-%d")
prevdayrange = today- timedelta(days=6)
start_date = prevdayrange.strftime("%Y-%m-%d")

def _color_red_or_green(val):
    color = '#9af764' if val > 0 else '#fc5a50'
    return 'background: %s' % color

def bar_with_plotly(stock):

    yf.pdr_override()
    #dwl_df = yf.download(tickers=stock, start=startdate, end=enddate, interval='1d',period='60d')
    dwl_df = yf.download(tickers=stock, period='1d', interval='5m')
    dwl_df.reset_index(inplace=True) 
    dwl_df[['Open','High','Low','Close','Adj Close']] = dwl_df[['Open','High','Low','Close','Adj Close']].round(2)

    dwl_df['fast_MA'] = dwl_df['Close'].ewm(span=fast_MA, adjust=False).mean()
    dwl_df['slow_MA'] = dwl_df['Close'].ewm(span=slow_MA, adjust=False).mean()
    dwl_df[['fast_MA','slow_MA']] = dwl_df[['fast_MA','slow_MA']].round(2)
    dwl_df['intersectionpoint'] = np.where(dwl_df['fast_MA'] > dwl_df['slow_MA'], 1.0, 0.0)
    dwl_df['Crossover'] = dwl_df['intersectionpoint'].diff()
    filtered_col_df = dwl_df[['Datetime','Open','High','Low','Close','Crossover']].copy()
    rslt_df = filtered_col_df[filtered_col_df['Crossover'] != 0.0] 
    rslt_df['Datetime'] = pd.to_datetime(rslt_df['Datetime'])
    rslt_df['Datetime'] = rslt_df['Datetime'].dt.strftime('%H:%M')
    rslt_df.insert(0,'Symbol','')
    rslt_df['Symbol'] = stock
    
    # Use render_template to pass graphJSON to html
    return rslt_df.tail(4)


@app.route('/') 
def bar_with_plotly1():
    length = len(stocksymbols)
    appended_data = pd.DataFrame()
    for x in stocksymbols:
        data = bar_with_plotly(x)
        appended_data = appended_data._append(data,ignore_index=True)
    appended_data = appended_data.sort_values(by='Datetime',ascending=[False])
    #appended_data['Crossover'] = appended_data['Crossover'].round(1)
    #styled_df = appended_data.style.set_properties(**{'background-color': 'red'})
    styled_df = appended_data.style.applymap(_color_red_or_green, subset=['Crossover'])
    #styled_df.style.hide_index()
    return """<meta http-equiv="refresh" content="300" />  {}.""".format(styled_df.to_html(index=False))
    #return styled_df.to_html(index=False)
 
