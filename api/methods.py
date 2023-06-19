import tweepy
import string
import time
import requests
from requests.structures import CaseInsensitiveDict
import json
import nltk
import os
import urllib.request as urllib
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('wordnet')
nltk.download('stopwords')

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

# def get_tweets(query, tweet_count=1000):
#     # Authenticate to Twitter
#     auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
#     auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#     # Create API object
#     api = tweepy.API(auth, wait_on_rate_limit=True)

#     # Use the Cursor object to get tweets matching the query
#     tweets = []
#     for tweet in tweepy.Cursor(api.search_tweets, q=query, lang='en', result_type='recent', tweet_mode='extended').items(tweet_count):
#         if 'retweeted_status' in dir(tweet):   # If it's a retweet
#             tweets.append(tweet.retweeted_status.full_text)
#         else:                                  # If it's a normal tweet
#             tweets.append(tweet.full_text)

#     # Return the tweets
#     return tweets

def get_tweets(query, tweet_count=1000):
    headers = CaseInsensitiveDict()
    headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    headers["User-Agent"] = "v2RecentSearchPython"

    base_url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&tweet.fields=text"
    url = base_url
    tweets = []

    while len(tweets) < tweet_count:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 429:  # Rate limit hit
            print(f"Rate limit hit. Waiting for 15 minutes")
            time.sleep(15*60)  # wait 15 minutes
            continue
        elif resp.status_code != 200:
            print(f"Response status code: {resp.status_code}")
            print(f"Response text: {resp.text}")
            raise ValueError("Failed to fetch tweets")

        data = resp.json()
        new_tweets = [tweet['text'] for tweet in data['data']]
        tweets.extend(new_tweets)

        # Check if there's more tweets to fetch
        if 'next_token' in data['meta']:
            next_token = data['meta']['next_token']
            url = base_url + f"&next_token={next_token}"
        else:
            break

    return tweets[:tweet_count] 

def getAttributes(url, tag, className):
    # Open the URL and parse the HTML using Beautiful Soup
    page = urllib.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    # Find the relevant HTML tag and id
    cabinet_list = soup.find('ul', {'id': 'cabinet'})

    # Check if cabinet_list was found
    if not cabinet_list:
        print("Cabinet list not found in HTML.")
        return []

    # Initialize an empty list to store text or dictionary objects
    textList = []

    # If tag is 'img', extract image and name information from each list item
    if tag == 'img':
        for cabinet_member in cabinet_list.find_all('li'):
            img = cabinet_member.find(tag)
            if img:
                img_src = img.get('src')
                textList.append(img_src)
    elif tag == 'h3':
        for cabinet_member in cabinet_list.find_all('li'):
            name = cabinet_member.find(tag, class_=className)
            if name:
                textList.append(name.text.strip())
            else:
                print(f"No {tag} with class {className} found in cabinet_member.")
    else:  # case for roles
        for cabinet_member in cabinet_list.find_all('li'):
            role_div = cabinet_member.find('div', class_=className)
            if role_div:
                role = role_div.find('p')
                if role:
                    textList.append(role.text.strip())
                else:
                    print(f"No p tag found in div with class {className}.")
            else:
                print(f"No div with class {className} found in cabinet_member.")

    # Return a list of text or dictionary objects
    return textList

# Cleaning the data

def remove_retweets(tweets):
    # Create a list to store the tweets without the retweet text
    tweets_without_retweets = []
    
    # Iterate over each tweet text
    for tweet in tweets:
        # Check if the tweet starts with "RT"
        if tweet.startswith("RT"):
            # Find the index of ":" in the tweet
            colon_index = tweet.index(":")
            
            # Remove the text between and including "RT" and ":" from the tweet
            tweet = tweet[colon_index + 1:]
        
        # Append the tweet without the retweet text to the list
        tweets_without_retweets.append(tweet)
    
    # Return the tweets without the retweet text
    return tweets_without_retweets

def lowercase_tweets(tweets):
    # Create a list to store the lowercased tweets
    lowercased_tweets = []
    
    # Iterate over each tweet text
    for tweet in tweets:
        # Lowercase the tweet text and append it to the list
        lowercased_tweets.append(tweet.lower())
    
    # Return the lowercased tweets
    return lowercased_tweets

def remove_punctuation(tweets):

    # Create a list to store the tweets without punctuation
    tweets_without_punctuation = []
    
    # Iterate over each lowercased tweet text
    for tweet in tweets:
        # Remove punctuation from the tweet text
        tweet_without_punctuation = tweet.translate(str.maketrans("", "", string.punctuation))
        
        # Append the tweet without punctuation to the list
        tweets_without_punctuation.append(tweet_without_punctuation)
    
    # Return the tweets without punctuation
    return tweets_without_punctuation

def remove_stop_words(tweets):
    # Get the English stop words
    stop_words = set(stopwords.words("english"))
    
    # Create a list to store the tweets without stop words
    tweets_without_stop_words = []
    
    # Iterate over each tweet text
    for tweet in tweets:
        # Tokenize the tweet text into words
        words = word_tokenize(tweet)
        
        # Remove stop words from the list of words
        words = [word for word in words if not word in stop_words]
        
        # Join the list of words back into a tweet text
        tweet_without_stop_words = " ".join(words)
        
        # Append the tweet without stop words to the list
        tweets_without_stop_words.append(tweet_without_stop_words)
    
    # Return the tweets without stop words
    return tweets_without_stop_words

def lemmatize_tweets(tweets):
    # Initialize the WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()

    # List to store the lemmatized tweets
    lemmatized_tweets = []

    # Iterate over each tweet text
    for tweet in tweets:
        # Tokenize the tweet text into words
        words = word_tokenize(tweet)
        # Lemmatize each word
        lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
        # Join the lemmatized words to form the lemmatized tweet
        lemmatized_tweet = " ".join(lemmatized_words)
        # Add the lemmatized tweet to the list of lemmatized tweets
        lemmatized_tweets.append(lemmatized_tweet)

    # Return the lemmatized tweets
    return lemmatized_tweets

def remove_duplicates(tweets_list):
    unique_tweets = []
    for tweet in tweets_list:
        if tweet not in unique_tweets:
            unique_tweets.append(tweet)
    return unique_tweets

# Sentiment Analysis

def sentiment_checker(tweets):
    
    # Create a SentimentIntensityAnalyzer object
    sentiment_analyzer = SentimentIntensityAnalyzer()
    
    # Keep track of the number of positive, negative, and neutral tweets
    positive_tweets = 0
    negative_tweets = 0
    neutral_tweets = 0
    
    # Iterate over each tweet
    for tweet in tweets:
        # Get the sentiment of the tweet
        sentiment = sentiment_analyzer.polarity_scores(tweet)
        
        # Increment the appropriate counter based on the sentiment score
        if sentiment['compound'] > 0:
            positive_tweets += 1
        elif sentiment['compound'] < 0:
            negative_tweets += 1
        else:
            neutral_tweets += 1
    
    # Calculate the total number of tweets
    total_tweets = positive_tweets + negative_tweets + neutral_tweets
    
    # Calculate the percentage of tweets that are positive, negative, and neutral
    try:
        positive_percentage = (positive_tweets / total_tweets) * 100
        negative_percentage = (negative_tweets / total_tweets) * 100
        neutral_percentage = (neutral_tweets / total_tweets) * 100
    except ZeroDivisionError:
        return {'positive_percentage': 0,
                'negative_percentage': 0,
                'neutral_percentage': 0}
    
    # Return the percentages
    return {'positive_percentage': round(positive_percentage, 1),
            'negative_percentage': round(negative_percentage, 1),
            'neutral_percentage': round(neutral_percentage, 1)}
