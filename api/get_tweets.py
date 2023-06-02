from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from methods import get_tweets
import os
from dotenv import load_dotenv
from datetime import datetime
import methods

load_dotenv()

Base = declarative_base()

class CabinetMinister(Base):
    __tablename__ = 'cabinet_ministers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    img_src = Column(String)


class Sentiment(Base):
    __tablename__ = 'sentiments'
    id = Column(Integer, primary_key=True)
    minister = Column(String)
    positive_score = Column(Numeric)
    negative_score = Column(Numeric)
    neutral_score = Column(Numeric)
    dateTime = Column(String)



engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)


def tweets(count):
    session = Session()
    all_tweets = {}

    for minister in session.query(CabinetMinister).all():
        tweets = get_tweets(minister.name, tweet_count=count)
        all_tweets[minister.name] = tweets

    return all_tweets


def clean_tweets(tweets_dict):
    cleaned_dict = {}

    for minister, tweets in tweets_dict.items():
        tweets = methods.remove_retweets(tweets)
        tweets = methods.lowercase_tweets(tweets)
        tweets = methods.remove_punctuation(tweets)
        tweets = methods.remove_stop_words(tweets)
        tweets = methods.lemmatize_tweets(tweets)
        cleaned_tweets = methods.remove_duplicates(tweets)
        
        cleaned_dict[minister] = cleaned_tweets

    return cleaned_dict

def analyse_tweets():
    session = Session()

    # Delete all existing rows in the CabinetMinister table
    session.query(Sentiment).delete()
    session.commit()

    # get tweets
    raw_tweets = tweets(1000)

    # Clean tweets
    cleaned_dict = clean_tweets(raw_tweets)

    # Iterate over each minister and their cleaned tweets
    for minister, cleaned_tweets in cleaned_dict.items():
        # Apply sentiment analysis to the cleaned tweets
        sentiment_result = methods.sentiment_checker(cleaned_tweets)

        # Create a new Sentiment object
        sentiment = Sentiment(
            minister=minister,
            positive_score=sentiment_result['positive_percentage'],
            negative_score=sentiment_result['negative_percentage'],
            neutral_score=sentiment_result['neutral_percentage'],
            dateTime=datetime.now().strftime('%d-%m-%Y %H:%M')
        )

        # Add the sentiment object to the session
        session.add(sentiment)

    # Commit the changes to the database
    session.commit()

    # Close the session
    session.close()


analyse_tweets()



