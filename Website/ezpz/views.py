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
from .forms import *
import base64
from base64 import b64decode
from django.core.files.base import ContentFile
import pickle
import numpy as np
import datetime
import json
import collections

from django.utils import timezone

def train_models(request):

	def train_consumer_feedback_model_tfidf():
		tfidf = tfidf_analysis.train_tfidf_from_file(ConsumerComplaints.bank, "Issue")
		pickle.dumps(tfidf)
		# tf = pickle.loads(pickled_model)
		# tfidf_analysis.get_tfid_score_from_paragraph(tf, "funds account bank")

	def train_consumer_feedback_model_nb():
		dataset = DataSet()
		dataset.format(ConsumerComplaints.all, "Issue", "Product") #Issue
		clf = classifiers.train_nb_classifier(dataset)
		TrainedModel.save_pickle(pickle.dumps(clf), "consumer_feedback_nb")


	def train_urgency_model_nb():
		dataset = DataSet()
		dataset.format(FEEDBACK_DATA_PATH, "Message", "Importance");
		clf = classifiers.train_nb_classifier(dataset)
		TrainedModel.save_pickle(pickle.dumps(clf), "urgency_nb")

	# train_consumer_feedback_model_nb()
	train_urgency_model_nb()
	print "trained"
	return HttpResponse("<h1>Training my model here...</h1>")

class IndexView(TemplateView):
	template_name = 'ezpz/main.html'

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
		# print dictionaries
		dictionaries = convertToString(dictionaries)
		print dictionaries
		return JsonResponse({"images": dictionaries}, safe=False)

	def post(self, request):
		# add a new image into database
		# data = json.loads(request.body)
		# imageFeedback = data['imageFeedback']
		if request.POST.get("image"):
			image_feedback = request.POST.get("image")
			# image_feedback = image_feedback.split('base64,', 1 )
			# print image_feedback
			# image_feedback = b64decode(image_feedback)
			format, imgstr = image_feedback.split(';base64,') 
			ext = format.split('/')[-1] 
			data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
			# print "imageFeedback: " + imageFeedback
			category = general_operations.get_image_classification(data)
			# category = "None"
			image_name = category
			score_dict = general_operations._get_priority_score_dict(category, datetime.datetime.now())
			priority = general_operations._get_priority_score(score_dict)
			image = ImageFeedback(image=data, category=category, date_created=timezone.now(), priority=priority)
			image.save()
			return JsonResponse({"success": True}, status=200)
		print "error with image form"
		return HttpResponse(status=404)

def get_image(request, year, month, day, image_name):
	src = "images/" + year + "/" + month + "/" + day + "/" + image_name
	image_data = open(src, "rb").read()
	return HttpResponse(image_data, content_type="image/png")
		
def convertToString(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convertToString, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convertToString, data))
    else:
        return data
