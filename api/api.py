import requests
import re
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import jsonify
from bs4 import BeautifulSoup
from flask import Flask, render_template
from urllib.request import urlopen

app = Flask(__name__)
cors = CORS(app)

def getQuery(search):
    response = requests.get(search)
    results = response.json()
    return jsonify(results)

# pmPageID = 24150
# HomeSecPageID = 149104
# query = 'https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&pageids={}'
# @app.route('/')
# @cross_origin()
# def index():
#     result = getQuery(query.format(HomeSecPageID))
#     return result 

url = 'https://www.gov.uk/government/ministers'
soup = BeautifulSoup(requests.get(url).text,'html.parser')

@app.route('/')
@cross_origin()
def index():
    html = urlopen('https://www.gov.uk/government/ministers')
    bs = getQuery(BeautifulSoup(html, 'html.parser'))
    return bs
