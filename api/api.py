import json
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import jsonify
from bs4 import BeautifulSoup
import urllib.request as urllib

# Import Flask and CORS libraries
app = Flask(__name__)
cors = CORS(app)

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
    if tag=='img':
        for cabinet_member in cabinet_list.find_all('li'):
            text = cabinet_member.find(tag)
            img = cabinet_member.find('img')
            if text and img:
                name_str = img.get('alt')
                img_src = img.get('src')
                textList.append({'name': name_str.replace('The Rt Hon ', ''), 'img_src': img_src})
    # Otherwise, extract text information with a given tag and class from each list item
    else:
        for cabinet_member in cabinet_list.find_all('li'):
            text = cabinet_member.find(tag, {'class': className})
            if text:
                textList.append(text.text)
    
    # Return a list of text or dictionary objects
    return textList

# Define function to write a list of objects to a file
def writeToFile(object, filename):
    # Open the file for writing
    with open(filename, "w") as f:
        # Loop through each item in the list
        for item in object:
            # If the item is a dictionary, convert it to a string with JSON
            if isinstance(item, dict):
                item = json.dumps(item)
            # Write the item to the file
            f.write(str(item) + "\n")

# Define the default route for the web application
@app.route('/')
@cross_origin()
def names():
    govPage = 'https://www.gov.uk/government/ministers'
    
    # Call the getAttributes function to extract names, roles, and images
    names = getAttributes(govPage, 'span','app-person-link__name')
    
    # Write the names, roles, and images to separate files
    writeToFile(names, "names.txt")
    
    # Return a JSON object containing the image URLs
    return jsonify(names)

@app.route('/roles')
@cross_origin()
def roles():
    govPage = 'https://www.gov.uk/government/ministers'
    
    # Call the getAttributes function to extract names, roles, and images
    roles = getAttributes(govPage, 'a','govuk-link')
    
    # Write the names, roles, and images to separate files
    writeToFile(roles, "roles.txt")
    
    # Return a JSON object containing the image URLs
    return jsonify(roles)

@app.route('/images')
@cross_origin()
def images():
    govPage = 'https://www.gov.uk/government/ministers'
    
    # Call the getAttributes function to extract names, roles, and images
    images = getAttributes(govPage, 'img','')
    
    # Write the names, roles, and images to separate files
    writeToFile(images, "images.txt")
    
    # Return a JSON object containing the image URLs
    return jsonify(images)