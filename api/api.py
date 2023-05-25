import methods
import json
import os
from database import db
from dotenv import load_dotenv
from flask import Flask
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
from flask import jsonify
from bs4 import BeautifulSoup
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.request as urllib
import nltk
import alembic.config
from datetime import datetime
from get_tweets import update_tweets

nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('wordnet')
nltk.download('stopwords')
load_dotenv()

# Import Flask and CORS libraries
app = Flask(__name__, static_folder='../build', static_url_path='')
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.init_app(app)

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
    
class Tweets(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    minister = Column(String)
    tweet = Column(String)
    
# Define function to scrape attributes from HTML using Beautiful Soup
def getAttributes(url, tag, className):
    # Open the URL and parse the HTML using Beautiful Soup
    page = urllib.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    # Find the relevant HTML tag and class
    cabinet_list = soup.find('ul', {'class': 'cabinet-list'})

    # Initialize an empty list to store text or dictionary objects
    textList = []

    # If tag is 'img', extract image and name information from each list item
    if tag == 'img':
        for cabinet_member in cabinet_list.find_all('li'):
            text = cabinet_member.find(tag)
            img = cabinet_member.find('img')
            if text and img:
                name_str = img.get('alt')
                img_src = img.get('src')
                textList.append({'name': name_str.replace(
                    'The Rt Hon ', ''), 'img_src': img_src})
    # Otherwise, extract text information with a given tag and class from each list item
    else:
        for cabinet_member in cabinet_list.find_all('li'):
            text = cabinet_member.find(tag, {'class': className})
            if text:
                textList.append(text.text)

    # Return a list of text or dictionary objects
    return textList

  
# Define the default route for the web application
@app.route('/ministers')
@cross_origin()
def getData():
    # Create a new session within the Flask app context
    with app.app_context():
        Session = sessionmaker(bind=db.engine)
        session = Session()

        govPage = 'https://www.gov.uk/government/ministers'

        # Call the getAttributes function to extract names, roles, and images
        names = getAttributes(govPage, 'span', 'app-person-link__name')
        roles = getAttributes(govPage, 'a', 'govuk-link')
        images = getAttributes(govPage, 'img', '')

        combined_list = []
        # Combine the names, roles, and images into a single list of dictionaries
        for name, role, image in zip(names, roles, images):
            combined_list.append({
                "name": name,
                "role": role,
                "img_src": image["img_src"]
            })

        # Delete all existing rows in the CabinetMinister table
        session.query(CabinetMinister).delete()
        session.commit()

        # Write the names, roles, and images to the CabinetMinister table
        for data in combined_list:
            minister = CabinetMinister(name=data['name'], role=data['role'], img_src=data['img_src'])
            session.merge(minister)

        session.commit()

        # Close the session
        session.close()

    return jsonify(combined_list)


@app.route('/sentiments')
@cross_origin()
def getSentiments():
    # Create a new session within the Flask app context
    with app.app_context():
        Session = sessionmaker(bind=db.engine)
        session = Session()

        # Query all tweets from the Tweets table
        tweets = session.query(Tweets).all()

        tweet_texts = {}

        for tweet in tweets:
            minister = tweet.minister
            if minister in tweet_texts:
                tweet_texts[minister].append(tweet.tweet)
            else:
                tweet_texts[minister] = [tweet.tweet]

        # Perform sentiment analysis on each tweet
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

        # Insert sentiment scores into the Sentiment table
        session.query(Sentiment).delete()
        for key, sentiment_scores in sentiments.items():
            positive_score = sentiment_scores['positive_percentage']
            negative_score = sentiment_scores['negative_percentage']
            neutral_score = sentiment_scores['neutral_percentage']

            sentiment = Sentiment(
                minister=key,
                positive_score=positive_score,
                negative_score=negative_score,
                neutral_score=neutral_score
            )
            session.add(sentiment)

        session.commit()

        # Close the session
        session.close()

    return jsonify(sentiments)

SECRET_TOKEN = os.getenv('SECRET_TOKEN')
current_date = datetime.today().strftime('%d-%m-%Y')
@app.route('/update_tweets', methods=['POST'])
def flask_update_tweets():
    auth_token = request.headers.get('Authorization')
    if auth_token == SECRET_TOKEN:
        update_tweets()  # Call the function that updates the tweets
        return f'Updated {current_date}', 200
    else:
        return 'Unauthorized', 403


@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000)) # Get the port number from the environment variable, or use 5000 as default
    alembic.config.main(argv=['--raiseerr','upgrade', 'head'])
    app.run(host='0.0.0.0', port=port)
