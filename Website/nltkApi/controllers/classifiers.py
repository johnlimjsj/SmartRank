from sklearn.naive_bayes import MultinomialNB
from nltkApi.controllers.tfidf_analysis import train_tfidftransformer_from_file
from sklearn.pipeline import Pipeline
from nltkApi.utils.data_loader import DataSet, FEEDBACK_DATA_PATH, QUESTIONS_DATA_PATH
from sklearn.metrics import *
from sklearn import svm
from sklearn.metrics import classification_report
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer

def train_svm_classifier(dataset):
	vectorizer = TfidfVectorizer(min_df=5, max_df = 0.8, sublinear_tf=True, use_idf=True)
	train_vectors = vectorizer.fit_transform(dataset.data)
	classifier_rbf = svm.SVC()
	classifier_rbf.fit(train_vectors, dataset.target)

	return classifier_rbf, vectorizer


def train_nb_classifier(dataset):
	text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()), ])
	text_clf = text_clf.fit(dataset.data, dataset.target)
	return text_clf

def get_classification_score_nb(clf, test_data):
	category = clf.predict([test_data])[0]
	score = clf.score([test_data], [category])
	return {'category': category, 'score': score}


def Question_Sentence_Match(question, threshold=0.3):
	dataset = DataSet()
	dataset.format_list(QUESTIONS_DATA_PATH, "Question")
	sum = 0
	count = len(dataset.data)
	cnt = 1
	for data in dataset.data:
		Question_Matcher = SequenceMatcher(None, data, question).ratio()
		if Question_Matcher > threshold:
			sum += Question_Matcher
			cnt += 1
	print "score is: ", sum/cnt
	return sum/cnt

















# Learning code for reference. DO not use

def train_nb_classifier_learn():
	X_train_tfidf, twenty_train, count_vect, tfidf_transformer = train_tfidftransformer_from_file("","")
	clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)
	clf2 = MultinomialNB();

	docs_new = ['God is love', 'OpenGL on the GPU is fast']
	X_new_counts = count_vect.transform(docs_new)
	X_new_tfidf = tfidf_transformer.transform(X_new_counts)

	text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()), ])
	text_clf = text_clf.fit(twenty_train.data, twenty_train.target)
	predicted = text_clf.predict(docs_new)
	for doc, category in zip(docs_new, predicted):
		print('%r => %s' % (doc, twenty_train.target_names[category]))
