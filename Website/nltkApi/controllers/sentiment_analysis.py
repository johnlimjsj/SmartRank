from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from nltkApi.utils.general import translate
from nltk import tokenize


def get_sentiment_score(paragraph):
	sentences = tokenize.sent_tokenize(paragraph)
	sid = SentimentIntensityAnalyzer()
	sensitivity_score = sid.polarity_scores(paragraph)

	if len(sentences) == 0:
		return 0

	for sentence in sentences:
		sensitivity_score = sid.polarity_scores(sentence)
		break

	score = translate(sensitivity_score['compound'], -1, 1, 0, 1, 2)
	return score



