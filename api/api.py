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
query = 'https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&pageids={}'
@app.route('/')
def index():
    result = getQuery(query2.format(pm))
    return result



