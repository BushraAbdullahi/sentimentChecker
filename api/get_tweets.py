from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from methods import get_tweets
import os
from dotenv import load_dotenv
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

engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
session = Session()

# Delete all existing rows in the CabinetMinister table
session.query(Tweets).delete()

session.commit()

for minister in session.query(CabinetMinister).all():
    minister_name = minister.name
    tweets = get_tweets(minister_name, tweet_count=5)  # Adjust tweet_count as needed

    for tweet in tweets:
        tweet_data = Tweets(minister=minister_name, tweet=tweet.full_text)
        session.add(tweet_data)

session.commit()



