# -*- coding: UTF-8 -*-
from pymongo import MongoClient 
from pymongo.errors import DuplicateKeyError

import nltk
from nltk.corpus import stopwords
from pattern.es import parse, split
import re

SPACE_PATTERN = re.compile("\s+")

def extract_topics_list(text):	
	words = re.split(SPACE_PATTERN, text)
	topic_words=[]
	for t in words:
		last_char = t[-1]
		if last_char in [',', ':', '.']:
			t= t[0:-1]
		topic_words.append(t)
	return topic_words


stop_words = stopwords.words('spanish')

client = MongoClient('localhost', 27017)
tweets_db = client['tweets']

tweets_db.trending_topics_tags.remove({});

tweets = tweets_db.tweets.find({})#.limit(10)
i=1;
for t in tweets:	
	i=i+1
	if(i%50 ==0):
		print i;	
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
			tag= tweets_db.trending_topics_tags.find_one({"tag": token_lowercase, "city_id":0, "candidate_id":0}) 

			if tag == None:
				tag={"city_id": 0, "candidate_id": 0, "tag": token_lowercase, "qty": 1}
				tweets_db.trending_topics_tags.insert(tag)
			else:
				tag['qty']=tag['qty']+1;
				tweets_db.trending_topics_tags.update({'_id': tag['_id']}, {"$set": tag}, upsert=False)
				
			if len(filter_p.keys())>0:
				filter_p['tag']= token_lowercase
				tag= tweets_db.trending_topics_tags.find_one(filter_p) 
				if tag == None:
					tag={"city_id": filter_p['city_id'], "candidate_id": filter_p['candidate_id'], "tag": filter_p['tag'], "qty": 1}
					tweets_db.trending_topics_tags.insert(tag)
				else:
					tag['qty']=tag['qty']+1;
					tweets_db.trending_topics_tags.update({'_id': tag['_id']}, {"$set": tag}, upsert=False)
		