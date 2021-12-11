from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import View

# Create your views here.
from django.http import HttpResponse
import yfinance as yf
import time
import datetime
import os
import json
import sys
import tweepy
from . import getTweets




class HomeView(View):
      def get(self, request):
        num_users = User.objects.count()
        login_url = ""
        return render(
            request,
            'stocktweetapp/login.html',
            {'login_url': login_url, 'num_users': num_users},
            )

def index(request):
	return render(request, 'stocktweetapp/index.html')

def login(request):
    	return render(request, 'stocktweetapp/login.html')





def search_stock(request):
    stock_name = ''

    if request.method == 'POST':
        stock_name = request.POST['search']
        stock_data = yf.Ticker(stock_name)
        stock_infor = stock_data.info
        output_dic = {}
        
        if 'dayHigh' not in stock_infor:
            output_dic['txt'] = "Sorry, please reenter the symbol for the stock or try this link"
            output_dic['linkToStockPage'] = f'https://finance.yahoo.com/quote/{stock_name}?p={stock_name}&.tsrc=fin-srch'
            #result = json.dumps(output_dic, indent = 4)
            context = output_dic
            return render(request, 'stockUnfound.html', context)
        
        output_dic['symbol'] = stock_name
        output_dic['name'] = stock_infor['longName']
        output_dic['currentPrice'] = stock_infor['currentPrice']
        output_dic['dayHigh'] = stock_infor['dayHigh']
        output_dic['dayLow'] = stock_infor['dayLow']
        output_dic['currency'] = stock_infor['currency']
        output_dic['recommendationKey'] = stock_infor['recommendationKey']
        output_dic['linkToStockPage'] = f'https://finance.yahoo.com/quote/{stock_name}?p={stock_name}&.tsrc=fin-srch'
        #result = json.dumps(output_dic, indent = 4)
        context = output_dic

        return render(request, 'stockResult.html', context)  
    else:
        return render(request, 'stocktweetapp/index.html')
    
    

#def stock_recommendation(request):
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


