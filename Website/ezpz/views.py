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

# Create your views here.

class IndexView(TemplateView):
	template_name = 'ezpz/main.html'

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