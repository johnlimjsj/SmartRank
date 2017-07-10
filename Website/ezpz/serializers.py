from rest_framework import serializers
from models import *

class GoodsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Goods
		fields = ('id', 'category', 'name', 'price', 'likes', 'rating')

class ServicesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Services
		fields = ('id', 'category', 'name', 'price', 'likes', 'rating')