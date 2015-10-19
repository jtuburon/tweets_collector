# -*- coding: UTF-8 -*-
from pymongo import MongoClient 
from pymongo.errors import DuplicateKeyError
import tweepy
import datetime
import time
import json

# assuming twitter_authentication.py contains each of the 4 oauth elements (1 per line)

## KIKI's TOKENS
API_KEY = '1PWVnEFibELmjReza0191JXIJ'
API_SECRET= 'YVIwKr2z0DjOwexufziwfiZ4OUumSOQRvrLDqVDJIagMP3jSte'
ACCESS_TOKEN = '1038975522-Y9jugcOJIMJMlBZh9gwgexCbjFD6spooVJ0AgXo'
ACCESS_TOKEN_SECRET = 'gJqUCASC0mOyGPWjqojOQiNOJES81itA3Euv3d4K5alHI'

## TEOS TOKENS
# API_KEY= 'KVLSoYq7kirTn5HK7Y17zWg7l'
# API_SECRET= 'ZIPTVmFjIcoU0k6miVvGj9NcusiEwVMrSieltsGTQ37iO5ulAa'
# ACCESS_TOKEN='3957965975-nYuzNqOyNhG2ceK2RoWUVQX2eueMWLDMmpKYyIO'
# ACCESS_TOKEN_SECRET='h57v6qpaBrxZf8Z4nzsOTzivH9wp76WcB2gBo22aGNDvi'

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

client = MongoClient('localhost', 27017)
tweets_db = client['tweets']
counter = tweets_db.followers_history.count()

candidates = tweets_db.candidates.find();
api = tweepy.API(auth_handler= auth, wait_on_rate_limit=True)

counter=counter+1
print "Counter"
print counter
for c in candidates:
	timestamp= str(datetime.datetime.now())
	followers=[]
	for user in tweepy.Cursor(api.followers, screen_name= c['account']).items():
		followers.append(user.screen_name);
	f_h={
		"history_id": counter,
		"candidate_id": c['candidate_id'],
		"timestamp": timestamp,
		"followers": followers 
	}
	tweets_db.followers_history.insert(f_h);