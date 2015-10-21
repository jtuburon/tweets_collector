# -*- coding: UTF-8 -*-
from pymongo import MongoClient 
from pymongo.errors import DuplicateKeyError
from datetime import datetime
from bson import SON
from datetime import datetime

epoch = datetime.utcfromtimestamp(0)

client = MongoClient('localhost', 27017)
tweets_db = client['tweets']
stats_list = []

epoch = datetime.utcfromtimestamp(0)
client = MongoClient('localhost', 27017)
tweets_db = client['tweets']
stats_list = []

candidates={}
for c in tweets_db.candidates.find():
	candidates[c['candidate_id']]= c['account']
	stats = tweets_db.followers_history.find({'candidate_id': c['candidate_id']}).sort([('history_id', 1)])#.limit(300)
	data=[]
	for s in stats:
		timestamp= s['timestamp']

		date_object = datetime.strptime(s['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
		print date_object.tzinfo
		print epoch
		print timestamp
		ms= int((date_object - epoch).total_seconds() * 1)
		print ms
		obj_d={
			"x": ms,
			"y": s['followers_count']
		}
		data.append(obj_d)

	obj={
		"name": c['account'],
		"data": data
	}
	stats_list.append(obj)
