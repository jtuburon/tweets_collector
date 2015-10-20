# -*- coding: UTF-8 -*-
from pymongo import MongoClient 
from pymongo.errors import DuplicateKeyError
import tweepy
import datetime
import time
import json

# assuming twitter_authentication.py contains each of the 4 oauth elements (1 per line)

## KIKI's TOKENS
API_KEY = '8tO9xnrbUm5qwSvv1csIEahQG'
API_SECRET= '2i8lskOnIl6mKQwNmtdk38ZseFNnPtqNuHc6hbidicRZpsLuZ8'
ACCESS_TOKEN = '1038975522-Y9jugcOJIMJMlBZh9gwgexCbjFD6spooVJ0AgXo'
ACCESS_TOKEN_SECRET = 'gJqUCASC0mOyGPWjqojOQiNOJES81itA3Euv3d4K5alHI'

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

client = MongoClient('localhost', 27017)
tweets_db = client['tweets']
counter = tweets_db.followers_history.count()

candidates = tweets_db.candidates.find();
api = tweepy.API(auth_handler= auth, wait_on_rate_limit=True)

counter=counter+1
print "Counter"
print datetime.datetime.now()
print counter
for c in candidates:
	print c
	timestamp= str(datetime.datetime.now())
	followers=[]
	user= api.get_user(c['account'])
	followers_count =user.followers_count
	f_h={
		"history_id": counter,
		"candidate_id": c['candidate_id'],
		"timestamp": timestamp,
		"followers_count": followers_count 
	}
	tweets_db.followers_history.insert(f_h);
print datetime.datetime.now()