from flask import Flask,jsonify,request,json,render_template
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import yfinance as yf

app = Flask(__name__) 

@app.route('/') 
def ReturnHome():
    return render_template('data.html')

