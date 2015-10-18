from pymongo import MongoClient 
from decimal import Decimal

client = MongoClient('localhost', 27017)
spanew_db = client['spanew']
spanew_db.words.remove({})
header=True;
file = open('SPANEW.csv', 'r')
for line in file:
	if not header:
		line= line.replace('\n', '')
		data= line.split(",")	
		word={
			"word": data[0], 
			"valence":{
				"mean": float(data[1]),
				"sd": float(data[2])
			},
			"arousal":{
				"mean": float(data[3]),
				"sd": float(data[4])
			},
			"dominance":{
				"mean": float(data[5]),
				"sd": float(data[6])
			}
		}
		print word
		spanew_db.words.insert(word)
	else:
		header=False