# -*- coding: UTF-8 -*-
import scipy.stats
import re

def calculate_overall_mean(spanew_words, variable):
    num_sum=0.0
    den_sum=0.0
    for w in spanew_words:
        mean = w[variable]["mean"]
        sd = w[variable]["sd"]
        normal_dist = scipy.stats.norm(mean, sd)
        norm_prob= normal_dist.pdf(mean)
        num_sum= num_sum + mean * norm_prob
        den_sum= den_sum + norm_prob
    if not (den_sum == 0):
        return num_sum/den_sum
    else:
        return None

def compute_tweet(tweet):
    words= re.compile('\w+').findall(tweet['text'])
    print words
    spanew_words=[]
    for word in words:
        spanew_word =spanew_db.words.find_one({"word": word})
        if spanew_word:
            spanew_words.append(spanew_word)
    print spanew_words
    if len(spanew_words)>=2:
        tweet_text = tweet['text']
        tweet_r= {
            "tweet_id": tweet['_id'],
            "v_m": calculate_overall_mean(spanew_words, "valence"),
            "a_m": calculate_overall_mean(spanew_words, "arousal")
        }
        print tweet_r
        #tweets_db.computed_tweets.insert(tweet_r)

def initSources():
    tweets_db.keywords.remove({})
    
    tweets_db.keywords.insert({"name": "Elecciones Bogotá", "last_retrieved_id": 0})
    tweets_db.keywords.insert({"name": "alcaldia bogota", "last_retrieved_id": 0})

    tweets_db.keywords.insert({"name": "Clara Lopez", "last_retrieved_id": 0})
    tweets_db.keywords.insert({"name": "@ClaraLopezObre" , "last_retrieved_id": 0})
    tweets_db.keywords.insert({"name": "#ClaraAlcaldesa", "last_retrieved_id": 0})
    tweets_db.keywords.insert({"name": "#estudiantesvotanclara", "last_retrieved_id": 0})

    tweets_db.keywords.insert({"name": "Rafael Pardo", "last_retrieved_id": 0})
    tweets_db.keywords.insert({"name": "@RafaelPardo", "last_retrieved_id": 0})
    tweets_db.keywords.insert({"name": "#seguroquesí", "last_retrieved_id": 0})
    tweets_db.keywords.insert({"name": "#BogotaOrganizada", "last_retrieved_id": 0})
    tweets_db.keywords.insert({"name": "#yovotopardo", "last_retrieved_id": 0})

    tweets_db.keywords.insert({"name": "Francisco Santos", "last_retrieved_id": 0})
    tweets_db.keywords.insert({"name": "@PachoSantosC", "last_retrieved_id": 0})
    tweets_db.keywords.insert({"name": "#cambioconseguridad", "last_retrieved_id": 0})
    tweets_db.keywords.insert({"name": "#yovotoporpacho", "last_retrieved_id": 0})

    tweets_db.keywords.insert({"name": "Enrique Peñaloza", "last_retrieved_id": 0})
    tweets_db.keywords.insert({"name": "@EnriquePenalosa", "last_retrieved_id": 0})
    tweets_db.keywords.insert({"name": "#yovotopenalosa", "last_retrieved_id": 0})
    tweets_db.keywords.insert({"name": "#recuperemosbogota", "last_retrieved_id": 0})