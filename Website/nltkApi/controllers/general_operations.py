from nltk import tokenize
from nltk.tokenize import RegexpTokenizer
import datetime
import math
from django.http import HttpResponse, JsonResponse
import json
from nltkApi.controllers import classifiers, sentiment_analysis, tfidf_analysis
from nltkApi.models import TrainedModel


def get_length_score(paragraph):
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(paragraph)
	sentences = tokenize.sent_tokenize(paragraph)
	score = math.exp(-(1.0 / len(sentences)))
	return score

def get_age(date_created):
	date_now = datetime.datetime.now()
	time_diff = date_now - date_created
	hours, remainder = divmod(time_diff.seconds, 3600)
	score = math.exp(-(1.0/hours))
	return hours, score

def _get_priority_score_dict(feedback):
	clf = TrainedModel.get_clf("urgency_nb")
	score_urgency = classifiers.get_classification_score_nb(clf, "feedback here")
	score_qn = classifiers.get_question_score(feedback)
	score_len = get_length_score(feedback)
	score_sentiment = sentiment_analysis.get_sentiment_score(feedback)
	return {'urgency': score_urgency, 'question': score_qn, 'length': score_len, 'sentiment':score_sentiment}

def _get_priority_score(score_dict):
	weights = {'urgency': 0.1, 'sentiment': 0.1, 'length': 0.2, 'question': 0.1}
	score = score_dict['urgency'] * weights['urgency'] + score_dict['sentiment'] * weights['sentiment'] + \
			score_dict['length'] * weights['length'] + score_dict['question'] * weights['question']
	return score






