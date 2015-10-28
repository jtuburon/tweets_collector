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

def add_word_in_dict(city_id, candidate_id, word):
	if city_id not in topics_tags.keys():
		topics_tags[city_id]={}
		city_obj= topics_tags[city_id]
		if candidate_id not in city_obj.keys():
			city_obj[candidate_id]={}
			candidate_obj= city_obj[candidate_id]
			if word not in candidate_obj:
				candidate_obj[word]=1
			else:
				candidate_obj[word]=candidate_obj[word] + 1
		else:
			candidate_obj= city_obj[candidate_id]
			if word not in candidate_obj:
				candidate_obj[word]=1
			else:
				candidate_obj[word]=candidate_obj[word] + 1
	else:
		city_obj= topics_tags[city_id]
		if candidate_id not in city_obj.keys():
			city_obj[candidate_id]={}
			candidate_obj= city_obj[candidate_id]
			if word not in candidate_obj:
				candidate_obj[word]=1
			else:
				candidate_obj[word]=candidate_obj[word] + 1
		else:
			candidate_obj= city_obj[candidate_id]
			if word not in candidate_obj:
				candidate_obj[word]=1
			else:
				candidate_obj[word]=candidate_obj[word] + 1


stop_words = stopwords.words('spanish')

client = MongoClient('localhost', 27017)
tweets_db = client['tweets']

tweets_db.trending_topics.remove({});

tweets = tweets_db.tweets.find(no_cursor_timeout=True)#.limit(10)
tweets_count = tweets_db.tweets.count()

i=1;
topics_tags= {}

for t in tweets:			
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
			add_word_in_dict(0, 0, token_lowercase)
			if len(filter_p.keys())>0:
				add_word_in_dict(filter_p['city_id'], filter_p['candidate_id'], token_lowercase)
	
	if(i%10000 ==0 or i==tweets_count):
		print i
		for k1 in topics_tags.keys():
			city_key= topics_tags[k1]
			for k2 in city_key.keys():
				candidate_key= city_key[k2]
				for k3 in candidate_key.keys():
					word_count= candidate_key[k3]					
					tag= tweets_db.trending_topics.find_one({"tag": k3, "city_id":k1, "candidate_id":k2}) 
					if tag == None:
						tag={"city_id": k1, "candidate_id": k2, "tag": k3, "qty": word_count}
						tweets_db.trending_topics.insert(tag)
					else:
						tag['qty']=tag['qty']+word_count;
						tweets_db.trending_topics.update({'_id': tag['_id']}, {"$set": tag}, upsert=False)

		topics_tags={}	
	i=i+1