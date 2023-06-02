import os
from database import db
from dotenv import load_dotenv
from flask import Flask
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
from flask import jsonify
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import alembic.config


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
    dateTime = Column(String)
        
@app.route('/ministers')
@cross_origin()
def getMinisters():
    # Create a new session within the Flask app context
    with app.app_context():
        Session = sessionmaker(bind=db.engine)
        session = Session()

        # Query the ministers data from the CabinetMinister table
        ministers = session.query(CabinetMinister).all()

        ministers_list = []

        for minister in ministers:
            ministers_list.append({
                "name": minister.name,
                "role": minister.role,
                "img_src": minister.img_src
            })

        # Close the session
        session.close()

        return jsonify(ministers_list)


@app.route('/sentiments')
@cross_origin()
def getSentiments():
    # Create a new session within the Flask app context
    with app.app_context():
        Session = sessionmaker(bind=db.engine)
        session = Session()

        # Query sentiment scores from the Sentiment table
        sentiments = session.query(Sentiment).all()

        sentiment_scores = {}

        for sentiment in sentiments:
            minister = sentiment.minister
            sentiment_scores[minister] = {
            "positive_percentage": float(sentiment.positive_score),
            "negative_percentage": float(sentiment.negative_score),
            "neutral_percentage": float(sentiment.neutral_score)            }

        # Close the session
        session.close()

    return jsonify(sentiment_scores)

@app.route('/display_date')
def display_date():
    with app.app_context():
        Session = sessionmaker(bind=db.engine)
        session = Session()

        # Query the sentiments table, order the data by id in descending order, and get the first entry
        last_entry = session.query(Sentiment).order_by(Sentiment.id.desc()).first()

        if last_entry:
            return f'Last Updated: {last_entry.dateTime}'
        else:
            return 'No data found', 404
        


@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000)) # Get the port number from the environment variable, or use 5000 as default
    alembic.config.main(argv=['--raiseerr','upgrade', 'head'])
    app.run(host='0.0.0.0', port=port)
