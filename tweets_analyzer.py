import scipy.stats
import re
from pymongo import MongoClient 


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


minimun_spanew_words_in_tweet = 2

client = MongoClient('localhost', 27017)
spanew_db = client['spanew']
tweets_db = client['tweets']
tweets_considered=[]

tweets = tweets_db.tweets.find({})
for tweet in tweets:
	words= re.compile('\w+').findall(tweet['text'])
	spanew_words=[]
	for word in words:
		spanew_word =spanew_db.words.find_one({"word": word})
		if spanew_word:
			spanew_words.append(spanew_word)
	ratio= len(spanew_words)
	if ratio>=2:
		tweet_text = tweet['text']
		tweet_r= {
			"tweet_id": tweet['_id'],
			"ratio": ratio,
			"v_m": calculate_overall_mean(spanew_words, "valence"),
			"a_m": calculate_overall_mean(spanew_words, "arousal")
		}
		if "city_id" in tweet.keys():
			tweet_r['city_id']=tweet['city_id']
		if "candidate_id" in tweet.keys():
			tweet_r['candidate_id']=tweet['candidate_id']
		tweets_db.computed_tweets.insert(tweet_r)

