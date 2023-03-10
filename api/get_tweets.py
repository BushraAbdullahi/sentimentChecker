import json
import methods

with open('json_files/combined_list.json') as f:
    ministers = json.load(f)

tweet_dict = {}
tweet_dict = {minister['name']: '' for minister in ministers}
     
for minister in ministers:
    tweet_dict[minister['name']] = methods.get_tweets(minister['name'])
    tweet_dict[minister['name']] = [tweet.full_text for tweet in tweet_dict[minister['name']]]

# Write tweet_dict to a JSON file
with open('json_files/tweet_dict.json', "w") as outfile:
    json.dump(tweet_dict, outfile)



