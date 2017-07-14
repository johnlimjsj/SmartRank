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
from nltkApi.utils.data_loader import ConsumerComplaints, DataSet
import pickle
import numpy as np

# Create your views here.
pickled_model = ""

def train_models(request):

	def train_consumer_feedback_model_tfidf():
		tfidf = tfidf_analysis.train_tfidf_from_file(ConsumerComplaints.bank, "Issue")
		pickle.dumps(tfidf)
		# tf = pickle.loads(pickled_model)
		# tfidf_analysis.get_tfid_score_from_paragraph(tf, "funds account bank")

	def train_consumer_feedback_model_nb():
		consumer_dataset = DataSet()
		consumer_dataset.format(ConsumerComplaints.all, "Issue", "Product")
		text_clf = classifiers.train_nb_classifier(consumer_dataset)
		pickle.dumps(text_clf)
		docs_new = ['God is love']
		predicted = text_clf.predict(docs_new)
		print predicted, np.mean(predicted == consumer_dataset.target)


	# train_consumer_feedback_model_nb()

	return HttpResponse("Training my model here...")

class IndexView(TemplateView):
	template_name = 'ezpz/main.html'
	# paragraph = "It was one of the worst movies I've seen, despite good reviews. Unbelievably bad acting!! Poor direction. It was a VERY poor production. The movie was bad. Very bad movie. VERY BAD movie. VERY BAD movie!"

	# classifiers.Question_Sentence_Match()

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