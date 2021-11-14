import tweepy
import time
import datetime
import os
import json
import sys
from keys import key
from keys import secret
from keys import user
from keys import passw

auth = tweepy.OAuthHandler(user, passw)
auth.set_access_token(key, secret)
api = tweepy.api(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

def getTweets(input, numTweets, days_ago):
    tweetList = []
    yesterday = datetime.datetime.now() - datetime.timedelta(days = days_ago)

    for tweet in tweepy.Cursor(api.search, q=input.strip('\n')+f' since:{yesterday.strftime("%Y-%m-%d")}', lang='en').items(numTweets):
        try:
            print(f'Tweet recieved; Text: \n {tweet.text} --- {tweet.user.screen_name} --- {tweet.created_at}')
        except tweepy.error.TweepError as er:
            print(er.reason)
        except StopIteration:
            break
    return tweetList

def store_tweets(passed_tweet_list, file):
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
    file_to_open = open(file, 'w')
    json.dump(tweetList, file_to_open, indent = 4, sort_keys = True)
    file_to_open.flush()
    file_to_open.close()

def retrieve_tweets(input, tweets_to_open, days_ago):
    tweets = getTweets(input, tweets_to_open, days_ago)
    store_tweets(tweets, 'CS411-Fall-21\\retrieved_tweets.json')