# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from serializers import *
from rest_framework import viewsets, generics
from django.core.paginator import Paginator
from rest_framework.decorators import list_route, detail_route
from rest_framework import filters
from nltkApi.controllers import sentiment_analysis, tfidf_analysis, classifiers, general_operations
from nltkApi.utils import nltk_token_operations
from nltkApi.utils.data_loader import ConsumerComplaints, DataSet, FEEDBACK_DATA_PATH, QUESTIONS_DATA_PATH
from nltkApi.models import TrainedModel
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
from django.utils import timezone
from django.views import View
import pickle
import numpy as np
import datetime
import json

from django.utils import timezone

def train_models(request):

	def train_consumer_feedback_model_tfidf():
		tfidf = tfidf_analysis.train_tfidf_from_file(ConsumerComplaints.bank, "Issue")
		pickle.dumps(tfidf)
		# tf = pickle.loads(pickled_model)
		# tfidf_analysis.get_tfid_score_from_paragraph(tf, "funds account bank")

	def train_consumer_feedback_model_nb():
		dataset = DataSet()
		dataset.format(ConsumerComplaints.all, "Issue", "Product")
		text_clf = classifiers.train_nb_classifier(dataset)
		pickle.dumps(text_clf)
		test_data = ['God is love']
		predicted = text_clf.predict(test_data)
		print predicted, np.mean(predicted == dataset.target)


	def train_urgency_model_nb():
		dataset = DataSet()
		dataset.format(FEEDBACK_DATA_PATH, "Message", "Importance");
		clf = classifiers.train_nb_classifier(dataset)
		TrainedModel.save_pickle(pickle.dumps(clf), "urgency_nb")

	# train_consumer_feedback_model_nb()
	train_urgency_model_nb()
	return HttpResponse("<h1>Training my model here...</h1>")

class IndexView(TemplateView):
	template_name = 'ezpz/main.html'

	paragraph = "I NEED loads of help. Please help me" # "It was one of the worst movies I've seen, despite good reviews. Unbelievably bad acting!! Poor direction. It was a VERY poor production. The movie was bad. Very bad movie. VERY BAD movie. VERY BAD movie!"
	paragraph_medium = "I need some help with activating my account. Several days ago, I tried logging in, but was unsuccessful over 3 attempts and then got locked out. Could I have some assistance with reactivating my account? "# "The damage caused by the Incident only marginally increases over time."
	paragraph_low = "Thanks for your help on this issue a couple of days back! I would like to commend you and your team on a job well done"
	question = "why don't you just find it in the target"
	question2 = "Several days ago, I tried logging in, but was unsuccessful over 3 attempts and then got locked out. Could I have some assistance with reactivating my account?"
	# classifiers.Question_Sentence_Match(question2)

	dataset = DataSet()
	dataset.format(FEEDBACK_DATA_PATH, "Message", "Importance");

	clf = TrainedModel.get_clf("urgency_nb")
	info = classifiers.get_classification_score_nb(clf, paragraph_medium)
	print info

	#
	# general_operations.get_age(datetime.datetime(2017, 6, 23, 16, 29, 43))

	@method_decorator(ensure_csrf_cookie)
	def dispatch(self, *args, **kwargs):
		return super(IndexView, self).dispatch(*args, **kwargs)

class GoodsViewSet(viewsets.ModelViewSet):

	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = ('category',)
	queryset = Goods.objects.all()
	serializer_class = GoodsSerializer


class GoodsManager(generics.ListAPIView):
    serializer_class = GoodsSerializer

    def get_queryset(self):
        category = self.kwargs['category']
        return Goods.objects.filter(category__iexact=category)

class ServicesViewSet(viewsets.ModelViewSet):

	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = ('category',)
	queryset = Services.objects.all()
	serializer_class = ServicesSerializer

class ServicesManager(generics.ListAPIView):
    serializer_class = ServicesSerializer

    def get_queryset(self):
        category = self.kwargs['category']
        return Services.objects.filter(category__iexact=category)


class ImageManager(View):
	def get(self, request):
		# return all images sorted by priority
		all_images = ImageFeedback.objects.all().order_by('-priority')
		dictionaries = [ obj.as_dict() for obj in all_images ]
		return JsonResponse(json.dumps({"images":dictionaries}), safe=False)

	def post(self, request):
		# add a new image into database
		# data = json.loads(request.body)
		# imageFeedback = data['imageFeedback']
		imageFeedback = request.FILES.get('imageFeedback')
		# category = general_operations.get_image_classification(imageFeedback)
		category = "None"
		priority = general_operations._get_priority_score(category)
		image = ImageFeedback(image=imageFeedback, category=category, date_created=timezone.now(), priority=priority)
		image.save()
		return JsonResponse({"success": True}, status=200)


