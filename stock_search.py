import yfinance as yf
import time
import datetime
import os
import json
import sys


def search_stock(stock_name):
    # search a stock with its symbol utilize yahoo! finance API and return relative information.
    stock_data = yf.Ticker(stock_name)
    stock_infor = stock_data.info
    output_dic = {}
    
    if 'dayHigh' not in stock_infor:
        output_dic['txt'] = "Sorry, please reenter the symbol for the stock or try this link"
        output_dic['linkToStockPage'] = f'https://finance.yahoo.com/quote/{stock_name}?p={stock_name}&.tsrc=fin-srch'
        result = json.dumps(output_dic, indent = 4)
        return result
    

    output_dic['symbol'] = stock_name
    output_dic['name'] = stock_infor['longName']
    output_dic['currentPrice'] = stock_infor['currentPrice']
    output_dic['dayHigh'] = stock_infor['dayHigh']
    output_dic['dayLow'] = stock_infor['dayLow']
    output_dic['currency'] = stock_infor['currency']
    output_dic['recommendationKey'] = stock_infor['recommendationKey']
    output_dic['linkToStockPage'] = f'https://finance.yahoo.com/quote/{stock_name}?p={stock_name}&.tsrc=fin-srch'
    result = json.dumps(output_dic, indent = 4)
    
    return result
    

    
