from nltk.corpus import subjectivity
from nltk.sentiment.util import *
from nltk import tokenize
from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import *
from collections import Counter


stemmer = PorterStemmer()

def stopword_removal(paragraph):
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(paragraph.lower())
	filtered_words = [word for word in tokens if word not in stopwords.words('english')]
	count = Counter(filtered_words)
	# print count.most_common(100)
	return filtered_words

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    return tokens
    stems = stem_tokens(tokens, stemmer)
    return stems


def sample():
	n_instances = 200

	subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
	obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
	print "subj docs", len(subj_docs), "obj docs", len(obj_docs)