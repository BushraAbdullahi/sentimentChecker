import requests
import re
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import jsonify
from bs4 import BeautifulSoup
from flask import app, make_response, render_template
import urllib.request as urllib

app = Flask(__name__)
cors = CORS(app)

def getQuery(search):
    response = requests.get(search)
    results = response.json()
    return jsonify(results)


@app.route('/')
@cross_origin()
def index():
    url = 'https://www.gov.uk/government/ministers'
    page = urllib.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    cabinet_list = soup.find('ul', {'class': 'cabinet-list'})
    names = []
    for cabinet_member in cabinet_list.find_all('li'):
        name = cabinet_member.find('span', {'class': 'app-person-link__name'})
        if name:
            names.append(name.text)
    return jsonify(names)