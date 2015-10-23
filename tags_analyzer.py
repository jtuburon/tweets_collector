# import nltk
# sentence = """los hombres libres proclaman libertad."""
# tokens = nltk.word_tokenize(sentence)
# print tokens
# tagged = nltk.pos_tag(tokens)
# print tagged

# from textblob import TextBlob

# blob = TextBlob(sentence)
# print blob.detect_language()
# print blob.tags

# from pattern.es import singularize, pluralize

# print singularize('gatos')

import re

sentence = """la @pelota #notienensabor http://127.0.0.1:8000/taller03app/ es, amarilla, y los hombres libres proclaman libertad."""
print sentence
pattern = re.compile("\s+")
pattern01 = re.compile(",$")

def extract_topics_list(text):	
	words = re.split(pattern, sentence)
	print words
topic_words=[]
for t in words:
	last_char = t[-1]
	if last_char in [',', ':', '.']:
		t= t[0:-1]
	print t
print topic_words