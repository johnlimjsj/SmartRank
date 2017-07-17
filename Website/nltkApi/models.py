from __future__ import unicode_literals

from django.db import models
import pickle

# Create your models here.

class TrainedModel(models.Model):
	name = models.CharField(max_length=255)
	pickled_name = models.CharField(max_length=6553600)

	def __str__(self):
		return self.name

	@classmethod
	def get_pickle(cls, name):
		try:
			saved_model = TrainedModel.objects.get(name=name)
			return saved_model.pickled_name
		except Exception as e:
			return


	@classmethod
	def get_clf(cls, name):
		try:
			pic_name = cls.get_pickle(name)
			return pickle.loads(pic_name)
		except Exception as e:
			print e
			return

	@classmethod
	def save_pickle_from_clf(cls, clf, name):
		cls.save_pickle(cls, pickle.dumps(clf), name)

	@classmethod
	def save_pickle(cls, pickled_name, name):

		if TrainedModel.objects.filter(name=name).count() < 1:
			my_pickle = cls.objects.create(name=name, pickled_name=pickled_name)
			my_pickle.save()

		else:
			saved_model = TrainedModel.objects.get(name=name)
		 	# Updating the pickle with the new saved model
			saved_model.pickled_name = pickled_name
			saved_model.save()



