# -*- coding: UTF-8 -*-
from pymongo import MongoClient 
from pymongo.errors import DuplicateKeyError

client = MongoClient('localhost', 27017)
tweets_db = client['tweets']

categories=[
	{	
		"city_id":1,
		"candidate_id":10,
		"keywords":["Clara Lopez","@ClaraLopezObre", "#ClaraAlcaldesa", "#estudiantesvotanclara"]
	},
	{	
		"city_id":1,
		"candidate_id":11,
		"keywords":["Rafael Pardo","@RafaelPardo", "#seguroquesí", "#BogotaOrganizada", "#yovotopardo"]
	},
	{	
		"city_id":1,
		"candidate_id":12,
		"keywords":["Francisco Santos", "@PachoSantosC", "#cambioconseguridad", "#yovotoporpacho"]
	},
	{
		"city_id":1,	
		"candidate_id":13,
		"keywords":["Enrique Peñaloza", "@EnriquePenalosa", "#yovotopenalosa", "#recuperemosbogota"]
	}
]

tweets= tweets_db.tweets.find({})
for t in tweets:
	for c in categories:
		for w in c['keywords']:
			if w in t['text'].encode("utf-8"):
				t['city_id']=c['city_id']
				t['candidate_id']=c['candidate_id']
				tweets_db.tweets.update({'_id': t['_id']}, {"$set": t}, upsert=False)