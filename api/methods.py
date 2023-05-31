import tweepy
import string
import nltk
import os
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

Api_key = os.getenv('Api_key')
API_secret_key = os.getenv('API_secret_key')
Access_Token = os.getenv('Access_Token')
Access_Token_Secret = os.getenv('Access_Token_Secret')

def get_tweets(query, tweet_count=5):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(Api_key, API_secret_key)
    auth.set_access_token(Access_Token, Access_Token_Secret)

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Use the Cursor object to get tweets matching the query
    tweets = []
    for tweet in tweepy.Cursor(api.search_tweets, q=query, lang='en', result_type='recent', tweet_mode='extended').items(tweet_count):
        if 'retweeted_status' in dir(tweet):   # If it's a retweet
            tweets.append(tweet.retweeted_status.full_text)
        else:                                  # If it's a normal tweet
            tweets.append(tweet.full_text)

    # Return the tweets
    return tweets


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
