# -*- coding: UTF-8 -*-
from pymongo import MongoClient 
from pymongo.errors import DuplicateKeyError



def initCities():    
    tweets_db.cities.remove({})
    tweets_db.cities.insert({"city_id": 1, "name": "Bogotá"})
    tweets_db.cities.insert({"city_id": 2, "name": "Cali"})
    tweets_db.cities.insert({"city_id": 3, "name": "Medellín"})
    tweets_db.cities.insert({"city_id": 4, "name": "Barranquilla"})
    
def initCandidates():    
    tweets_db.candidates.remove({})

    tweets_db.candidates.insert({"candidate_id": 10, "city_id": 1, "name": "Clara Lopez", "account":"@ClaraLopezObre"})
    tweets_db.candidates.insert({"candidate_id": 11, "city_id": 1, "name": "Rafael Pardo", "account":"@RafaelPardo"})
    tweets_db.candidates.insert({"candidate_id": 12, "city_id": 1, "name": "Francisco Santos", "account":"@PachoSantosC"})
    tweets_db.candidates.insert({"candidate_id": 13, "city_id": 1, "name": "Enrique Peñaloza", "account":"@EnriquePenalosa"})

    tweets_db.candidates.insert({"candidate_id": 20, "city_id": 2, "name": "Angelino Garzon", "account": "@Angelino_Garzon"})
    tweets_db.candidates.insert({"candidate_id": 21, "city_id": 2, "name": "roberto ortiz", "account": "@robertoortizu"})
    tweets_db.candidates.insert({"candidate_id": 22, "city_id": 2, "name": "maurice armitage", "account": "@MauriceArmitage"})
    tweets_db.candidates.insert({"candidate_id": 23, "city_id": 2, "name": "maria isabel urrutia", "account": "@MariaIsaUrrutia"})
    tweets_db.candidates.insert({"candidate_id": 24, "city_id": 2, "name": "carlos josé holguin", "account": "@carlosjholguin"})
    tweets_db.candidates.insert({"candidate_id": 25, "city_id": 2, "name": "wilson arias", "account": "@wilsonariasc"})

    tweets_db.candidates.insert({"candidate_id": 30, "city_id": 3, "name": "Eugenio Prieto", "account": "@EugenioPrieto"})
    tweets_db.candidates.insert({"candidate_id": 31, "city_id": 3, "name": "Juan Carlos Velez", "account": "@jcvelezuribe "})
    tweets_db.candidates.insert({"candidate_id": 32, "city_id": 3, "name": "Alonso Salazar", "account": "@AlcaldeAlonsoS"})
    tweets_db.candidates.insert({"candidate_id": 33, "city_id": 3, "name": "Federico Gutierrez", "account": "@FicoGutierrez"})
    tweets_db.candidates.insert({"candidate_id": 34, "city_id": 3, "name": "Gabriel Jaime Rico", "account": "@RICOGabriel"})

client = MongoClient('localhost', 27017)
tweets_db = client['tweets']
initCities();
initCandidates();