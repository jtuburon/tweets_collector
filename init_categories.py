# -*- coding: UTF-8 -*-
from pymongo import MongoClient 
from pymongo.errors import DuplicateKeyError

categories=[
	{	
		"city_id":1,
		"candidate_id":10,
		"keywords":[
		    #{"name": "Clara Lopez", "last_retrieved_id": 0},
		    {"name": "@ClaraLopezObre" , "last_retrieved_id": 0}
		    #{"name": "#ClaraAlcaldesa", "last_retrieved_id": 0},
		    #{"name": "#estudiantesvotanclara", "last_retrieved_id": 0}
		]
	},
	{	
		"city_id":1,
		"candidate_id":11,
		"keywords":[
			#{"name": "Rafael Pardo","last_retrieved_id": 0},
			{"name": "@RafaelPardo", "last_retrieved_id": 0}
			#{"name": "#seguroquesí", "last_retrieved_id": 0},
			#{"name": "#BogotaOrganizada", "last_retrieved_id": 0},
			#{"name": "#yovotopardo", "last_retrieved_id": 0}
		]
	},
	{	
		"city_id":1,
		"candidate_id":12,
		"keywords":[
			#{"name": "Francisco Santos", "last_retrieved_id": 0},
			{"name": "@PachoSantosC", "last_retrieved_id": 0}
			#{"name": "#cambioconseguridad", "last_retrieved_id": 0},
			#{"name": "#yovotoporpacho", "last_retrieved_id": 0}
		]
	},
	{
		"city_id":1,	
		"candidate_id":13,
		"keywords":[
			#{"name": "Enrique Peñaloza", "last_retrieved_id": 0},
			{"name": "@EnriquePenalosa", "last_retrieved_id": 0}
			#{"name": "#yovotopenalosa", "last_retrieved_id": 0},
			#{"name": "#recuperemosbogota", "last_retrieved_id": 0}
		]
	},
	

	{
		"city_id":2,	
		"candidate_id":20,
		"keywords":[
			{"name": "@Angelino_Garzon", "last_retrieved_id": 0},
		]
	},
	{
		"city_id":2,	
		"candidate_id":21,
		"keywords":[
			{"name": "@robertoortizu", "last_retrieved_id": 0},
		]
	},
	{
		"city_id":2,	
		"candidate_id":22,
		"keywords":[
			{"name": "@MauriceArmitage", "last_retrieved_id": 0},
		]
	},
	{
		"city_id":2,	
		"candidate_id":23,
		"keywords":[
			{"name": "@MariaIsaUrrutia", "last_retrieved_id": 0},
		]
	},
	{
		"city_id":2,	
		"candidate_id":24,
		"keywords":[
			{"name": "@carlosjholguin", "last_retrieved_id": 0},
		]
	},
	{
		"city_id":2,	
		"candidate_id":25,
		"keywords":[
			{"name": "@wilsonariasc", "last_retrieved_id": 0},
		]
	},


	{
		"city_id":3,	
		"candidate_id":30,
		"keywords":[
			{"name": "@EugenioPrieto", "last_retrieved_id": 0},
		]
	},
	{
		"city_id":3,	
		"candidate_id":31,
		"keywords":[
			{"name": "@jcvelezuribe", "last_retrieved_id": 0},
		]
	},
	{
		"city_id":3,	
		"candidate_id":32,
		"keywords":[
			{"name": "@AlcaldeAlonsoS", "last_retrieved_id": 0},
		]
	},
	{
		"city_id":3,	
		"candidate_id":33,
		"keywords":[
			{"name": "@FicoGutierrez", "last_retrieved_id": 0},
		]
	},
	{
		"city_id":3,	
		"candidate_id":34,
		"keywords":[
			{"name": "@RICOGabriel", "last_retrieved_id": 0},
		]
	}
]

client = MongoClient('localhost', 27017)

tweets_db = client['tweets']

tweets_db.categories.remove({})

for c in categories:
	tweets_db.categories.insert(c)