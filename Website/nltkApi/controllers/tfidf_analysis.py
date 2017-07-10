import string
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
from nltkApi.utils import data_loader, nltk_token_operations
from nltkApi.utils.nltk_token_operations import *
import logging
logging.basicConfig()

def get_tfid_score_from_paragraph(tfidf, paragraph):
	response = tfidf.transform([paragraph])
	print response
	feature_names = tfidf.get_feature_names()
	total = 0
	for col in response.nonzero()[1]:
		print feature_names[col], ' - ', response[0, col]
		total += response[0, col]
	print "total is:", total
	return total

def train_tfidf_from_file(file_dir, column):
	print "starting tfid training"
	with open(file_dir) as csvfile:
		tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
		readFile = csv.DictReader(csvfile)
		complaint_list = []
		for row in readFile:
			if row[column] != "" and row[column] is not None:
				try:
					formatted_str = row[column].lower().translate(None, string.punctuation).strip()
					complaint_list.append(formatted_str)
				except Exception as e:
					print e
					print "model was not successfully trained"
					return
		tfidf.fit(complaint_list)
		print "model trained"
		return tfidf

def train_tfidftransformer_from_file(file_dir, column):
	categories = ['alt.atheism', 'soc.religion.christian','comp.graphics', 'sci.med']
	from sklearn.datasets import fetch_20newsgroups
	twenty_train = fetch_20newsgroups(subset='train',categories=categories, shuffle=True, random_state=42)
	print twenty_train.data[100:101]
	print twenty_train.target[100:101]
	print twenty_train.target_names[0]
	count_vect = CountVectorizer()
	X_train_counts = count_vect.fit_transform(twenty_train.data)
	tfidf_transformer = TfidfTransformer()
	X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
	return X_train_tfidf, twenty_train, count_vect, tfidf_transformer
