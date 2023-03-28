import json
import methods
import os
from flask import Flask
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
from flask import jsonify
from bs4 import BeautifulSoup
import urllib.request as urllib
import nltk
nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('wordnet')
nltk.download('stopwords')

# Import Flask and CORS libraries
app = Flask(__name__, static_folder='../build')
CORS(app)

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

# Define function to write a list of objects to a file
def writeToFile(data_list, filename):
    # Open the file for writing
    with open(filename, "w") as f:
        # Write the data list as a JSON array to the file
        json.dump(data_list, f)

# Define the default route for the web application
@app.route('/ministers')
@cross_origin()
def getData():
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
    # Write the names, roles, and images to separate files
    writeToFile(combined_list, "json_files/combined_list.json")

    # Return a JSON object containing the image URLs
    return jsonify(combined_list)

@app.route('/sentiments')
@cross_origin()
def getSentiments():
    # Load the tweets from the JSON file
    with open('json_files/tweet_dict.json') as f:
        tweet_texts = json.load(f)

    # Iterate over the keys of the tweet_texts dictionary and clean the tweets
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

    # Write tweet_dict to a JSON file
    with open('json_files/sentiments.json', "w") as outfile:
        json.dump(sentiments, outfile)
    
    return jsonify(sentiments)


@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000)) # Get the port number from the environment variable, or use 5000 as default
    app.run(host='0.0.0.0', port=port)