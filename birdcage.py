# Kicked off using the code in this example...
# https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
import os, errno
import requests
import sys
import re
import tweepy
import json
import unidecode
import time
from tweepy import OAuthHandler
from datetime import date, datetime
from os.path import join, dirname

from modules.get_tweets import get_tweets
from modules.get_hashtag import get_hashtag

if __name__ == '__main__':

    # Accessing .env variables using `source .env`.
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_KEY')
    access_token_secret = os.getenv('ACCESS_SECRET')
    
    # API Authorization
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

	# Pass in the username of the account you want to download
    rawInput = sys.argv[1]

    # @ means get users tweets and media
    # Nothing means get hastags
    appCommand = rawInput[0][0] 
    inputTerm = rawInput[1:]
    directoryName = ''

    if appCommand == '@':
        directoryName = inputTerm
        # Create directory
        if not os.path.exists(inputTerm):
            os.makedirs(inputTerm)
            os.makedirs(inputTerm+"/media")

            if not os.path.exists(inputTerm+"/"):
                os.makedirs(inputTerm+"/")

        # Twitter only allows access to a users most recent 3240 tweets with this method
        print('RETRIEVING USER: '+rawInput)
        get_tweets(inputTerm, api)

        # --------------------------------------------------------------------------
        # ADDITIONAL FEATURES - uncomment as necessary
        # -----------------------------------------------------------------------------
        # get_followers(inputTerm)
        # get_favorites(inputTerm)
        # get_friends(inputTerm)

    else:
        directoryName = rawInput
        # Create directories
        if not os.path.exists(rawInput):
            os.makedirs(rawInput)
            os.makedirs(rawInput+"/media")

            if not os.path.exists(rawInput+"/"):
                os.makedirs(rawInput+"/")
                # get_tweets(inputTerm)

        print('RETRIEVING HASHTAG: '+rawInput)
        get_hashtag(api, rawInput)
