from sklearn.naive_bayes import MultinomialNB
from nltkApi.controllers.tfidf_analysis import train_tfidftransformer_from_file
from sklearn.pipeline import Pipeline
from nltkApi.utils.data_loader import DataSet, FEEDBACK_DATA_PATH, QUESTIONS_DATA_PATH
from sklearn.metrics import *
from sklearn import svm
from sklearn.metrics import classification_report
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
from nltk import tokenize


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

def get_classification_nb(clf, test_data):
	category = clf.predict([test_data])[0]
	score = clf.score([test_data], [category])
	return {'category': category, 'score': score}


def get_classification_score_nb(clf, test_data):
	info = get_classification_nb(clf, test_data)
	category = info['category']
	score = info['score']
	if (category == 'High'):
		score = 0.7 + 0.3 * score
	elif (category == 'Medium'):
		score = 0.5
	else:
		score = 0.3 - 0.3 * score

	return score

def get_question_score(question):
	info_qn = Question_Sentence_Match(question)
	return sum(info_qn['list_scores'])


def Question_Sentence_Match(question, threshold=0.3):
	dataset = DataSet()
	dataset.format_list(QUESTIONS_DATA_PATH, "Question")
	count = 0
	list_questions = []
	list_scores = []
	sentences = tokenize.sent_tokenize(question)
	# use tokenizer to break up the question into paragraphs. Then find if anything in the paragraph is a question
	for sentence in sentences:
		for data in dataset.data:
			score = SequenceMatcher(None, data, sentence).ratio()
			if sentence not in list_questions:
				if score > threshold:
					#if question has been added before, then don't add again
					list_questions.append(sentence)
					list_scores.append(score)
					count += 1

	return {'num_questions': count, 'list_questions': list_questions, 'list_scores': list_scores}

















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
