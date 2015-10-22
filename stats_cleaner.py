# -*- coding: UTF-8 -*-
from pymongo import MongoClient 
from pymongo.errors import DuplicateKeyError
from datetime import datetime
from bson import SON
from datetime import datetime

epoch = datetime.utcfromtimestamp(0)

client = MongoClient('localhost', 27017)
tweets_db = client['tweets']

data= tweets_db.followers_history.aggregate(
	[
	 {
	   "$group":
	     {
	       "_id": "$history_id",
	       "count": {"$sum": 1},
	     }
	},
	{"$sort": SON([("_id", 1)])}	
]);

for d in data:
	if d['count'] != 15:
		tweets_db.followers_history.remove({'history_id': d['_id']})
	else:
		print d['count']