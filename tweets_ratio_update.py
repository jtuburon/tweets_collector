# -*- coding: UTF-8 -*-
from pymongo import MongoClient 
import re

client = MongoClient('localhost', 27017)
tweets_db = client['tweets']
spanew_db = client['spanew']


computed_tweets= tweets_db.computed_tweets.find()
for c_t in computed_tweets:
	tweet = tweets_db.tweets.find_one({'_id': c_t['tweet_id']})
	
	words= re.compile('\w+').findall(tweet['text'])
	spanew_words=[]
	for word in words:
		spanew_word =spanew_db.words.find_one({"word": word})
		if spanew_word:
			spanew_words.append(spanew_word)

	ratio= len(spanew_words)
	c_t['ratio']=ratio
	tweets_db.computed_tweets.update({'_id': c_t['_id']}, {"$set": c_t}, upsert=False)