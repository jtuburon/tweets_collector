# -*- coding: UTF-8 -*-
from pymongo import MongoClient 
from pymongo.errors import DuplicateKeyError
import tweepy
import json
import scipy.stats
from nltk.corpus import stopwords
import re

SPACE_PATTERN = re.compile("\s+")
stop_words = stopwords.words('spanish')

def extract_topics_list(text):  
    words = re.split(SPACE_PATTERN, text)
    topic_words=[]
    for t in words:
        last_char = t[-1]
        if last_char in [',', ':', '.']:
            t= t[0:-1]
        topic_words.append(t)
    return topic_words

def compute_trending_topics(t):
    text=  t['text']
    filter_p= {}
    if 'city_id' in t.keys():
        filter_p['city_id']= t['city_id']
    if 'candidate_id' in t.keys():
        filter_p['candidate_id']= t['candidate_id']

    #tokens = nltk.word_tokenize(text)
    tokens = extract_topics_list(text)
    exclusion_tokens=["", " ", "rt"]

    for token in tokens:
        token_lowercase= token.lower()
        if token_lowercase not in stop_words and token_lowercase not in exclusion_tokens and len(token_lowercase)>1:
            tag= tweets_db.trending_topics.find_one({"tag": token_lowercase, "city_id":0, "candidate_id":0}) 
            if tag == None:
                tag={"city_id": 0, "candidate_id": 0, "tag": token_lowercase, "qty": 1}
                tweets_db.trending_topics.insert(tag)
            else:
                tag['qty']=tag['qty']+1;
                tweets_db.trending_topics.update({'_id': tag['_id']}, {"$set": tag}, upsert=False)
                
            if len(filter_p.keys())>0:
                filter_p['tag']= token_lowercase
                tag= tweets_db.trending_topics.find_one(filter_p) 
                if tag == None:
                    tag={"city_id": filter_p['city_id'], "candidate_id": filter_p['candidate_id'], "tag": filter_p['tag'], "qty": 1}
                    tweets_db.trending_topics.insert(tag)


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
            searched_tweets = api.search(q=keyword['name'], since_id=keyword['last_retrieved_id'], count=100)    
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
                    compute_trending_topics(tweet_obj)
                except Exception as e:
                   pass
            if len(searched_tweets)>0:
                keyword['last_retrieved_id']=searched_tweets[0].id
                tweets_db.categories.update({'_id': c['_id']}, {"$set": c}, upsert=False)
