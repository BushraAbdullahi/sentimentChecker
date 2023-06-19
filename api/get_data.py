from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import methods
import os
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

Base = declarative_base()

class CabinetMinister(Base):
    __tablename__ = 'cabinet_ministers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    img_src = Column(String)
    dateTime = Column(String)

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

# def write_tweets_to_json(raw_tweets, filename='tweets.json'):
#     with open(filename, 'w') as f:
#         json.dump(raw_tweets, f)
        
def tweets(count):
    session = Session()
    all_tweets = {}
    combined_list = session.query(CabinetMinister).all()  # Get the ministers in the desired order

    for minister in combined_list:
        query_name = minister.name.replace('CBE', '').replace('KC', '').strip()
        tweets = methods.get_tweets(query_name, tweet_count=count)
        all_tweets[minister.name] = tweets
        print(f'Collected {len(tweets)} tweets for {query_name}.')
        
    print(f'Collected {sum([len(tweets) for tweets in all_tweets.values()])} tweets.')
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

def scrape_and_store_ministers():
    session = Session()
    govPage = 'https://www.gov.uk/government/ministers'
    
    names = methods.getAttributes(govPage, 'h3', 'gem-c-image-card__title govuk-heading-s')
    roles = methods.getAttributes(govPage, 'p', 'gem-c-image-card__description')
    images = methods.getAttributes(govPage, 'img', '')
    
    combined_list = []
    for name, role, image in zip(names, roles, images):
        combined_list.append({
            "name": name,
            "role": role,
            "img_src": image,
            "dateTime": datetime.now().strftime('%d-%m-%Y %H:%M')
        })

    session.query(CabinetMinister).delete()
    session.commit()
    print('Old ministers deleted from the database.')
    print(f'List of Ministers scraped: {[item["name"] for item in combined_list]}')
    
    for data in combined_list:
        minister = CabinetMinister(name=data['name'], role=data['role'], img_src=data['img_src'], dateTime=data['dateTime'])
        session.merge(minister)

    session.commit()
    session.close()


def analyse_tweets():
    raw_tweets = tweets(100)
    cleaned_dict = clean_tweets(raw_tweets)
    for minister, cleaned_tweets in cleaned_dict.items():
        session = Session()
        session.query(Sentiment).filter(Sentiment.minister == minister).delete()
        sentiment_result = methods.sentiment_checker(cleaned_tweets)
        sentiment = Sentiment(minister=minister, positive_score=sentiment_result['positive_percentage'], negative_score=sentiment_result['negative_percentage'], neutral_score=sentiment_result['neutral_percentage'], dateTime=datetime.now().strftime('%d-%m-%Y %H:%M'))
        session.add(sentiment)
        session.commit()
        print(f'Sentiment analysis completed for {minister}.')
        session.close()

scrape_and_store_ministers()
analyse_tweets()
