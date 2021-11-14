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

    