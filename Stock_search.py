# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 14:20:09 2021

@author: we609
"""

import yfinance as yf
import time
import datetime
import os
import json
import sys


def search_stock(stock_name):
    
    stock_data = yf.Ticker(stock_name)


    stock_infor = stock_data.info
    output_dic = {}
    output_dic['symbol'] = stock_name
    output_dic['name'] = stock_infor['longName']
    output_dic['currentPrice'] = stock_infor['currentPrice']
    output_dic['dayHigh'] = stock_infor['dayHigh']
    output_dic['dayLow'] = stock_infor['dayLow']
    output_dic['currency'] = stock_infor['currency']
    output_dic['recommendationKey'] = stock_infor['recommendationKey']
    output_dic['linkToStockPage'] = f'https://finance.yahoo.com/quote/{stock_name}?p={stock_name}&.tsrc=fin-srch'
    stock_infor.json = json.dumps(output_dic, indent = 4)
    
    return stock_infor.json
    

    