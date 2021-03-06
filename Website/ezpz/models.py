# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

class Goods(models.Model):
	category = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	likes = models.IntegerField()
	rating = models.DecimalField(max_digits=2, decimal_places=1)

class Services(models.Model):
	category = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	price = models.CharField(max_length=255)
	likes = models.IntegerField()
	rating = models.DecimalField(max_digits=2, decimal_places=1)

class Feedback(models.Model):
	feedback = models.CharField(max_length=65536)
	date_created = models.DateTimeField() # should have the time stamp when it is created
	priority = models.FloatField(null=True)

	@classmethod
	def create(cls, feedback):
		cls.objects.create(feedback=feedback, date_created = timezone.now())

	@classmethod
	def get_all_sorted_descending(cls):
		all_feedback = Feedback.objects.all().order_by('-priority')
		return all_feedback

class ImageFeedback(models.Model):
	image = models.ImageField(upload_to='images/%Y/%m/%d')
	category = models.CharField(max_length=65536, null=True)
	date_created = models.DateTimeField()
	priority = models.FloatField()

	def as_dict(self):
		return {
			'image': self.image.url,
			'category': self.category,
			'date_created': self.date_created.isoformat(),
			'priority': self.priority
		}