# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

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


class Users(models.Model):
	name = models.CharField(max_length=255)
	age = models.IntegerField()
	designation = models.CharField(max_length=255)

class Feedback(models.Model):
	user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
	feedback = models.CharField(max_length=65536)
	date_created = models.TimeField() # should have the time stamp when it is created
	priority = models.FloatField()

