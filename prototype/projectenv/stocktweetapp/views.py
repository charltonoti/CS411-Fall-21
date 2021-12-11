from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import View
from stocktweetapp.models import Recommendations
# Create your views here.
from django.http import HttpResponse
import yfinance as yf
import time
from datetime import date
import datetime
import os
import json
import sys
import tweepy
import ast




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
    
    

def stock_recommendation(request):
    today = str(date.today())
    queryset = Recommendations.objects.filter(pub_date=today)
    
    if queryset.exists():
        
        context = ast.literal_eval(queryset[0].daily_recommemdation)
        return render(request, 'stock_recommendation.html', context)
    
        
        
    key = 'GAnoBnljxpISjDcJQxauB4tK3'
    secret = 'MHDLF4CqMKLpFcKJyi06d3JtoSD762V9Ure7cjr1Uv7kvj7Eu5'
    consumer_key = '1292952619611295763-vRbnOUfy3d03dlWgw9nGY0IhhY8ham'
    consumer_secret = 'dowgafj1COfeKmOwt1gqdCDGHFuqC8gAWgtyWgKErqXx1'
    auth = tweepy.OAuthHandler(key, secret)
    auth.set_access_token(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True)
    recommended_stocks = popular_stocks('stock_list', api)
    result = {}
    index = ['first','second', 'thrid','fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'nineth', 'tenth']
    for i in range(len(index)):
        stock_data = yf.Ticker(recommended_stocks[i])
        current_infor = stock_data.info['longName'] + " Symbol: " + recommended_stocks[i]
        result[index[i]] = current_infor
    context = result
    save_result = Recommendations(daily_recommemdation = str(result), pub_date = today)
    save_result.save()
    return render(request, 'stock_recommendation.html', context)
    
    
    
    
    
    
    
    
    
    
def getTweets(input_, numTweets, days_ago, api):
    #getting tweets
    tweetList = []
    yesterday = datetime.datetime.now() - datetime.timedelta(days = days_ago)
    sanitized_input = input_.strip('\n')+f' since:{yesterday.strftime("%Y-%m-%d")}'
    for tweet in tweepy.Cursor(api.search_tweets, q=sanitized_input, lang='en', result_type='popular').items(numTweets):
        try:
            #print(f'Tweet recieved; Text: \n {tweet.text} --- {tweet.user.screen_name} --- {tweet.created_at}')
            tweetList.append(tweet)
        except tweepy.error.TweepError as er:
            print(er.reason)
        except StopIteration:
            break
    return tweetList

    

def process_tweets(passed_tweet_list):
    # extract neccesary information from tweets
    tweetList = []
    for tweet in passed_tweet_list:
        tweet_info = dict()
        tweet_info['text'] = tweet.text
        tweet_info['creation'] = tweet.created_at.strftime("%m-%d-%Y %H:%M:%S")
        tweet_info['screen_name'] = tweet.user.screen_name
        tweet_info['retweet_count'] = tweet.retweet_count
        tweet_info['likes'] = tweet.favorite_count
        tweet_info['followers_count'] = tweet.user.followers_count
        tweetList.append(tweet_info)
    return tweetList
    

def popular_stocks(stock_list, api):
    #calculate the stock likes according to recent popular stock twitter
    stock_list = ['AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'TSLA', 'FB', 'NVDA', 'TSM', 'JPM', 'UNH', 'JNJ', 'HD', 'WMT', 'BAC', 'PG', 
                  'BABA', 'AMSL', 'ADBE', 'PFE', 'ORCL', 'DIS', 'NTES', 'NFLX', 'NKE', 'XOM', 'CRM', 'NVO', 'AVGO', 'TMO', 'CSCO', 'ACN', 
                  'PEP', 'PYPL', 'CMCSA', 'ABBV', 'QCOM', 'WFC', 'BLK', 'SCHW', 'TMUS', 'AXP', 'CHTR', 'AMT', 'UNH', 'ADBE', 'NTES', 'NVDA', 
                  'JPM', 'WMT', 'CVX', 'VZ']
    stocks_like = []
    
    for name in stock_list:
        symbol = name.split()[0]
        tweets = getTweets(symbol, 10, 1, api)
        tweet_infor = process_tweets(tweets)
        current_like = 0
        for i in tweet_infor:
            current_like += int(i['likes'])
        
        stocks_like += [[current_like, symbol]]
        
    stocks_like.sort()
    result = []
    
    for i in range(10):
        result += [stocks_like[-i-1][1]]
    return result
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


