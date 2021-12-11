import tweepy
import time
import datetime
import os
import json
import sys

import yfinance as yf

key = 'GAnoBnljxpISjDcJQxauB4tK3'
secret = 'MHDLF4CqMKLpFcKJyi06d3JtoSD762V9Ure7cjr1Uv7kvj7Eu5'
consumer_key = '1292952619611295763-vRbnOUfy3d03dlWgw9nGY0IhhY8ham'
consumer_secret = 'dowgafj1COfeKmOwt1gqdCDGHFuqC8gAWgtyWgKErqXx1'

auth = tweepy.OAuthHandler(key, secret)
auth.set_access_token(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

def getTweets(input_, numTweets, days_ago):
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
    

def popular_stocks(stock_list):
    #calculate the stock likes according to recent popular stock twitter
    stock_list = open(stock_list,'r')
    stocks_like = []
    
    for name in stock_list:
        symbol = name.split()[0]
        tweets = getTweets(symbol, 10, 1)
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
    
def main(key,secret,consumer_key,consumer_secret):
    auth = tweepy.OAuthHandler(key, secret)
    auth.set_access_token(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True)
    result = popular_stocks('stock_list')
    return result
    
    
    

    

