import requests
import json
import re
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import jsonify
from bs4 import BeautifulSoup
from flask import app, make_response, render_template
import urllib.request as urllib

app = Flask(__name__)
cors = CORS(app)

def getAttributes(url, tag, className):
    page = urllib.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    cabinet_list = soup.find('ul', {'class': 'cabinet-list'})
    textList = []
    
    if tag=='img':
        for cabinet_member in cabinet_list.find_all('li'):
            text = cabinet_member.find(tag)
            img = cabinet_member.find('img')
            if text and img:
                # Extract the text and src attribute from the tag and img
                name_str = img.get('alt')
                img_src = img.get('src')
                # Append a dictionary with the text and img src to the textList
                textList.append({'name': name_str.replace('The Rt Hon ', ''), 'img_src': img_src})
    else:
        for cabinet_member in cabinet_list.find_all('li'):
            text = cabinet_member.find(tag, {'class': className})
            if text:
                textList.append(text.text)
    return textList

def writeToFile(object, filename):
    with open(filename, "w") as f:
        for item in object:
            # If item is a dictionary, convert it to a JSON string
            if isinstance(item, dict):
                item = json.dumps(item)
            f.write(str(item) + "\n")


@app.route('/')
@cross_origin()
def index():
    govPage = 'https://www.gov.uk/government/ministers'
    names = getAttributes(govPage, 'span','app-person-link__name')
    roles = getAttributes(govPage, 'a','govuk-link')
    images = getAttributes(govPage, 'img','')
    writeToFile(names, "names.txt")
    writeToFile(roles, "roles.txt")
    writeToFile(images, "images.txt")
    return jsonify(images)