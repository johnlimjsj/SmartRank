from sklearn.naive_bayes import MultinomialNB
from nltkApi.controllers.tfidf_analysis import train_tfidftransformer_from_file
from sklearn.pipeline import Pipeline
from sklearn.metrics import *
from sklearn import svm
import time
from sklearn.metrics import classification_report
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer

def train_svm_classifier(dataset):
	vectorizer = TfidfVectorizer(min_df=5, max_df = 0.8, sublinear_tf=True, use_idf=True)
	train_vectors = vectorizer.fit_transform(dataset.data)
	classifier_rbf = svm.SVC()
	classifier_rbf.fit(train_vectors, dataset.target)


	return classifier_rbf, vectorizer





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

def train_nb_classifier(dataset):
	text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()), ])
	text_clf = text_clf.fit(dataset.data, dataset.target)
	return text_clf


Sample_Questions = ["what is the weather like","where are we today","why did you do that","where is the dog","when are we going to leave","why do you hate me","what is the Answer to question 8",
                    "what is a dinosour","what do i do in an hour","why do we have to leave at 6.00", "When is the apointment","where did you go","why did you do that","how did he win","why won't you help me",
                    "when did he find you","how do you get it","who does all the shipping","where do you buy stuff","why don't you just find it in the target","why don't you buy stuff at target","where did you say it was",
                    "when did he grab the phone","what happened at seven am","did you take my phone","do you like me","do you know what happened yesterday","did it break when it dropped","does it hurt everyday",
                    "does the car break down often","can you drive me home","where did you find me"
                    "can it fly from here to target","could you find it for me"]


def Question_Sentence_Match():
	print "question matching"
	for Ran_Question in Sample_Questions:
		Question_Matcher = SequenceMatcher(None, Ran_Question, "can you help me with this problem").ratio()
		if Question_Matcher > 0.5:
			print (Question_Matcher)
			print ("Similar to Question: "+Ran_Question)
			print ("likely a Question")
