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
