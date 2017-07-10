from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from nltk import tokenize
from nltk.tokenize import RegexpTokenizer


def get_length_score(paragraph):
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(paragraph)
	sentences = tokenize.sent_tokenize(paragraph)
	return {"num_sentences": len(sentences), "num_words": len(tokens)}


def get_sentiment_score(paragraph):
	sentences = tokenize.sent_tokenize(paragraph)
	sid = SentimentIntensityAnalyzer()
	sensitivity_score = sid.polarity_scores(paragraph)
	print "paragraph negativity", sensitivity_score['neg']

	for sentence in sentences:
		sensitivity_score = sid.polarity_scores(sentence)
		# print ss['neg']
		# for k in sorted(ss):
		# 	print('{0}: {1}, '.format(k, ss[k]))
	return sensitivity_score



