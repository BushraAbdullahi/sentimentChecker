import nltk
import json
import methods
nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('wordnet')
nltk.download('stopwords')

# Load the tweets from the JSON file
with open('./json_files/tweet_dict.json') as f:
    tweet_texts = json.load(f)

# Iterate over the keys of the tweet_texts dictionary and clean the tweets
for key in tweet_texts:
    tweet_texts[key] = methods.remove_retweets(tweet_texts[key])
    tweet_texts[key] = methods.lowercase_tweets(tweet_texts[key])
    tweet_texts[key] = methods.remove_punctuation(tweet_texts[key])
    tweet_texts[key] = methods.remove_stop_words(tweet_texts[key])
    tweet_texts[key] = methods.lemmatize_tweets(tweet_texts[key])
    tweet_texts[key] = methods.remove_duplicates(tweet_texts[key])
    
sentiments = {}
for tweet_key in tweet_texts.keys():
    sentiments[tweet_key] = None

for key in sentiments:
    sentiments[key] = methods.sentiment_checker(tweet_texts[key])

# Write tweet_dict to a JSON file
with open('./json_files/sentiments.json', "w") as outfile:
    json.dump(sentiments, outfile)