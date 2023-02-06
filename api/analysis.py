from textblob import TextBlob
# import sys
import tweepy
# import matplotlib.pyplot as plt
import pandas as pd
# import os
# import nltk
# import pycountry
import re
# import string
# from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
# from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from sklearn.feature_extraction.text import CountVectorizer

consumerKey = 'bPLWMtnUuH6xkh9nlfniMiNZZ'
consumerSecret = 'ARlA2pElm81JNmvg35yYFVSK4zwl4QBuiLouICtoLRzqDEJZKt'
accessToken = '1574560272399859715-JCkuEZoHCgTJxN7QJqD79qB6JsYUa4'
accessTokenSecret = '0sJdBHuNBzucxgeU6et4p5tyOgfjwB2esAV9zRMwMH0kC'

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

# Sentiment Analysis


def percentage(part, whole):
 return 100 * float(part)/float(whole)


keyword = input('Please enter keyword or hashtag to search: ')
noOfTweet = 1000
tweets = tweepy.Cursor(api.search_30_day(q=keyword) ).items(noOfTweet)

positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []

for tweet in tweets:
 # print(tweet.text)
 tweet_list.append(tweet.text)
 analysis = TextBlob(tweet.text)
 score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
 neg = score["neg"]
 neu = score["neu"]
 pos = score["pos"]
 comp = score["compound"]
 polarity += analysis.sentiment.polarity

if neg > pos:
    negative_list.append(tweet.text)
    negative += 1
elif pos > neg:
    positive_list.append(tweet.text)
    positive += 1

elif pos == neg:
    neutral_list.append(tweet.text)
    neutral += 1
 
positive = percentage(positive, noOfTweet)
negative = percentage(negative, noOfTweet)
neutral = percentage(neutral, noOfTweet)
polarity = percentage(polarity, noOfTweet)
positive = format(positive, '.1f')
negative = format(negative, '.1f')
neutral = format(neutral, '.1f')

tweet_list.drop_duplicates(inplace = True)

#Cleaning Text (RT, Punctuation etc)
#Creating new dataframe and new features
tw_list = pd.DataFrame(tweet_list)
tw_list['text'] = tw_list[0]
#Removing RT, Punctuation etc
remove_rt = lambda x: re.sub('RT @\w+: ',' ',x)
rt = lambda x: re.sub('(@[A-Za-z0–9]+)|([⁰-9A-Za-z \t])|(\w+:\/\/\S+)',' ',x)
tw_list['text'] = tw_list.text.map(remove_rt).map(rt)
tw_list['text'] = tw_list.text.str.lower()
tw_list.head(10)