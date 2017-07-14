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
from nltkApi.controllers import sentiment_analysis, tfidf_analysis, classifiers
from nltkApi.utils import nltk_token_operations
from nltkApi.utils.data_loader import ConsumerComplaints, DataSet, FEEDBACK_DATA_PATH
from nltkApi.models import TrainedModel
import pickle
import numpy as np


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


	def train_urgency_model_svc():
		dataset = DataSet()
		dataset.format(FEEDBACK_DATA_PATH, "Message", "Importance");
		clf = classifiers.train_nb_classifier(dataset)

		TrainedModel.save_pickle(pickle.dumps(clf), "urgency_svm")

		test_data = [' I would like to commend you and your team on a job well done'] #['My company is in the business of commodity trading, and so our work is highly time sensitive.']
		# test_vectors = vectorizer.transform(test_data)
		# predicted = clf.predict(test_data)




	# train_consumer_feedback_model_nb()
	train_urgency_model_svc()
	return HttpResponse("<h1>Training my model here...</h1>")

class IndexView(TemplateView):
	template_name = 'ezpz/main.html'
	paragraph = "It was one of the worst movies I've seen, despite good reviews. Unbelievably bad acting!! Poor direction. It was a VERY poor production. The movie was bad. Very bad movie. VERY BAD movie. VERY BAD movie!"

	classifiers.Question_Sentence_Match()

	clf = TrainedModel.get_clf("urgency_svm")
	# print clf.predict([paragraph])

	# retrieved_tfidf_model = pickle.loads(pickled_model)
	# sentiment_analysis.get_tfid_of_paragraph(retrieved_tfidf_model, paragraph)

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