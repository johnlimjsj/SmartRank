from nltk import tokenize
from nltk.tokenize import RegexpTokenizer
import datetime
import math
from django.http import HttpResponse, JsonResponse
import json
from nltkApi.controllers import classifiers, sentiment_analysis, tfidf_analysis
from nltkApi.models import TrainedModel

# from keras.applications import ResNet50
# from keras.applications import InceptionV3
# from keras.applications import Xception # TensorFlow ONLY
from keras.applications import VGG16
# from keras.applications import VGG19
from keras.applications import imagenet_utils
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
import numpy as np
import argparse


AGE_WEIGHT = 0.1
URGENCY_WEIGHT = 0.5
SENTIMENT_WEIGHT = 0.3
LENGTH_WEIGHT = 0.05
QUESTION_WEIGHT = 0.05

def get_length_score(paragraph):
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(paragraph)
	sentences = tokenize.sent_tokenize(paragraph)
	score = math.exp(-(1.0 / (0.45*len(sentences))))
	return score

def get_age_score(date_created):
	date_now = datetime.datetime.now()
	time_diff = date_now - date_created
	hours, remainder = divmod(time_diff.seconds, 3600)
	score = math.exp(-(1.0/(hours+0.0001))) # need small offset if not math error
	return score

def _get_priority_score_dict(feedback, date_created):
	clf = TrainedModel.get_clf("urgency_nb")
	score_urgency = classifiers.get_classification_score_nb(clf, feedback)
	score_qn = classifiers.get_question_score(feedback)
	score_len = get_length_score(feedback)
	score_sentiment = sentiment_analysis.get_sentiment_score(feedback)
	score_age = get_age_score(date_created)
	return {'urgency': score_urgency, 'question': score_qn, 'length': score_len, 'sentiment': score_sentiment, 'age': score_age}

def _get_priority_score(score_dict):
	score = score_dict['urgency'] * URGENCY_WEIGHT + score_dict['sentiment'] * SENTIMENT_WEIGHT + score_dict['length'] * LENGTH_WEIGHT + score_dict['question'] * QUESTION_WEIGHT + score_dict['age'] * AGE_WEIGHT

	print score_dict
	print score
	return score

def get_image_classification(imageData):
	# USAGE
	# python classify_image.py --image images/soccer_ball.jpg --model vgg16

	# define a dictionary that maps model names to their classes
	# inside Keras
	MODELS = {
		"vgg16": VGG16
	}

	# initialize the input image shape (224x224 pixels) along with
	# the pre-processing function (this might need to be changed
	# based on which model we use to classify our image)
	inputShape = (224, 224)
	preprocess = imagenet_utils.preprocess_input

	# load our the network weights from disk (NOTE: if this is the
	# first time you are running this script for a given network, the
	# weights will need to be downloaded first -- depending on which
	# network you are using, the weights can be 90-575MB, so be
	# patient; the weights will be cached and subsequent runs of this
	# script will be *much* faster)
	print("[INFO] loading {}...".format("vgg16"))
	
	Network = MODELS["vgg16"]
	model = Network(weights="imagenet")

	print "image data is", imageData

	# load the input image using the Keras helper utility while ensuring
	# the image is resized to `inputShape`, the required input dimensions
	# for the ImageNet pre-trained network
	print("[INFO] loading and pre-processing image...")
	image = load_img(imageData, target_size=inputShape)
	image = img_to_array(image)

	# our input image is now represented as a NumPy array of shape
	# (inputShape[0], inputShape[1], 3) however we need to expand the
	# dimension by making the shape (1, inputShape[0], inputShape[1], 3)
	# so we can pass it through thenetwork
	image = np.expand_dims(image, axis=0)

	# pre-process the image using the appropriate function based on the
	# model that has been loaded (i.e., mean subtraction, scaling, etc.)
	image = preprocess(image)

	# classify the image
	print("[INFO] classifying image with '{}'...".format("vgg16"))
	preds = model.predict(image)
	P = imagenet_utils.decode_predictions(preds)

	most_likely_label = ""

	# loop over the predictions and display the rank-5 predictions +
	# probabilities to our terminal
	for (i, (imagenetID, label, prob)) in enumerate(P[0]):
		if(i==0):
			most_likely_label = label
		print("{}. {}: {:.2f}%".format(i + 1, label, prob * 100))

	# load the image via OpenCV, draw the top prediction on the image,
	# and display the image to our screen
	# orig = cv2.imread(imageData)
	# (imagenetID, label, prob) = P[0][0]
	# cv2.putText(orig, "Label: {}, {:.2f}%".format(label, prob * 100),
	# 	(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
	# cv2.imshow("Classification", orig)
	# cv2.waitKey(0)

	return most_likely_label





