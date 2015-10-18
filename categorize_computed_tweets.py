# -*- coding: UTF-8 -*-
from pymongo import MongoClient 
from pymongo.errors import DuplicateKeyError

client = MongoClient('localhost', 27017)
tweets_db = client['tweets']

tweets= tweets_db.computed_tweets.find({})
for c_t in tweets:
	t = tweets= tweets_db.tweets.find_one({'_id': c_t['tweet_id']})
	if 'city_id' in t.keys():
		c_t['city_id']=t['city_id']
		c_t['candidate_id']=t['candidate_id']
		tweets_db.computed_tweets.update({'_id': c_t['_id']}, {"$set": c_t}, upsert=False)