import requests
from flask import Flask
from flask import jsonify

app = Flask(__name__)
def getQuery(search):
    response = requests.get(search)
    results = response.json()
    return jsonify(results)

pm = 24150
# query = 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&pageids={}&formatversion=2'
query2 = 'https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&pageids={}'
@app.route('/')
def index():
    result = getQuery(query2.format(pm))
    return result 

# https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&sites=enwiki&props=claims&titles=Prime%20Minister%20of%20the%20United%20Kingdom

