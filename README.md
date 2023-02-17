# UK Cabinet Ministers Sentiment Score App

This project is a web application that displays information about UK Cabinet Ministers. The front-end is built using React and the back-end is built using Flask. The app displays multiple cards that show the name, image, and Twitter sentiment score of each UK Cabinet Minister. The information is automatically updated as new sentiment scores become available.

## Getting Started

To run this app on your local machine, follow the steps below:

1. Clone the repository by running: git clone git@github.com:BushraAbdullahi/sentimentChecker.git
2. Make sure you're in the frontend directory: sentimentChecker
3. Install the necessary packages: npm install
4. Run this command: export FLASK_APP=api.py
5. Navigate to the backend directory: cd api
6. Install virtualenv: pip3 install virtualenv
7. Set up a virtual environment: virtualenv venv
8. Activate venv: source venv/bin/activate
9. Install the necessary packages: pip3 install -r requirements.txt
10. Start the front and back-end servers: npm start
11. Open your browser and navigate to http://localhost:3000

## How it Works
The app queries the web to get the names and images of incumbent UK Cabinet Ministers. It then uses Tweepy to get the latest tweets for each minister and nltk to perform sentiment analysis on the tweets. The sentiment score is then displayed on the app along with the minister's name and image.

The back-end server runs a Flask application that serves as an API for the front-end. The front-end sends requests to the back-end API to get the latest sentiment scores and information for each minister.

## Contributing

If you would like to contribute to this project, please follow the steps below:

* Fork the repository
* Create a new branch for your changes: git checkout -b your-feature
* Make your changes and test them thoroughly
* Push your changes to your forked repository: git push origin your-feature
* Submit a pull request to the original repository

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
