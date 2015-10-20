# -*- coding: UTF-8 -*-
from pymongo import MongoClient 
from pymongo.errors import DuplicateKeyError
import tweepy
import json
import scipy.stats
import re


def calculate_overall_mean(spanew_words, variable):
    num_sum=0.0
    den_sum=0.0
    for w in spanew_words:
        mean = w[variable]["mean"]
        sd = w[variable]["sd"]
        normal_dist = scipy.stats.norm(mean, sd)
        norm_prob= normal_dist.pdf(mean)
        num_sum= num_sum + mean * norm_prob
        den_sum= den_sum + norm_prob
    if not (den_sum == 0):
        return num_sum/den_sum
    else:
        return None

def compute_tweet(tweet):
    words= re.compile('\w+').findall(tweet['text'])
    spanew_words=[]
    for word in words:
        spanew_word =spanew_db.words.find_one({"word": word})
        if spanew_word:
            spanew_words.append(spanew_word)
    ratio= len(spanew_words)
    if ratio>=2:
        tweet_text = tweet['text']
        tweet_r= {
            "tweet_id": tweet['_id'],
            "city_id": tweet['city_id'],
            "candidate_id": tweet['candidate_id'],
            "ratio": ratio,
            "v_m": calculate_overall_mean(spanew_words, "valence"),
            "a_m": calculate_overall_mean(spanew_words, "arousal")
        }
        tweets_db.computed_tweets.insert(tweet_r)

# assuming twitter_authentication.py contains each of the 4 oauth elements (1 per line)
API_KEY= 'KVLSoYq7kirTn5HK7Y17zWg7l'
API_SECRET= 'ZIPTVmFjIcoU0k6miVvGj9NcusiEwVMrSieltsGTQ37iO5ulAa'
ACCESS_TOKEN='3957965975-nYuzNqOyNhG2ceK2RoWUVQX2eueMWLDMmpKYyIO'
ACCESS_TOKEN_SECRET='h57v6qpaBrxZf8Z4nzsOTzivH9wp76WcB2gBo22aGNDvi'

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth_handler= auth, wait_on_rate_limit=True)

client = MongoClient('localhost', 27017)

tweets_db = client['tweets']
spanew_db = client['spanew']

while True:
    print "ITERATION"
    for c in tweets_db.categories.find():
        for keyword in c['keywords']:
            searched_tweets = api.search(q=keyword['name'], since_id=keyword['last_retrieved_id'])    
            print keyword['name']
            print len(searched_tweets)
            print ""
            for tweet in searched_tweets:
                json_data = json.loads(json.dumps(tweet._json))
                json_data['city_id']=c['city_id']
                json_data['candidate_id']=c['candidate_id']
                try:
                    tweets_db.tweets.insert(json_data)
                    tweet_obj= tweets_db.tweets.find_one({'id': json_data['id']});
                    compute_tweet(tweet_obj)
                except Exception as e:
                   pass
            if len(searched_tweets)>0:
                keyword['last_retrieved_id']=searched_tweets[0].id
                tweets_db.categories.update({'_id': c['_id']}, {"$set": c}, upsert=False)
