from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from methods import get_tweets
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

Base = declarative_base()

class CabinetMinister(Base):
    __tablename__ = 'cabinet_ministers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    img_src = Column(String)
    
class Tweets(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    minister = Column(String)
    tweet = Column(String)
    dateTime = Column(String)


engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)

def update_tweets(session):
    # Delete all existing rows in tweets table
    session.query(Tweets).delete()
    session.commit()

    for minister in session.query(CabinetMinister).all():
        minister_name = minister.name
        tweets = get_tweets(minister_name, tweet_count=1000)
        for tweet in tweets:
            current_datetime = datetime.now().strftime('%d-%m-%Y %H:%M')
            tweet_data = Tweets(minister=minister_name, tweet=tweet.full_text, dateTime=current_datetime)
            session.add(tweet_data)

    session.commit()
    
