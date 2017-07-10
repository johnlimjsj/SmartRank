import csv
import string
import os

DATA_ROOT_PATH = "ezpz/static/ezpz/data/"
TRAINING_DATA_ROOT = DATA_ROOT_PATH + "training_data/"
TEST_DATA_ROOT = DATA_ROOT_PATH + "test_data/"

class ConsumerComplaints:

	def __generate_path_from_train(fileName):
		return TRAINING_DATA_ROOT + fileName

	bank = __generate_path_from_train("Consumer_Complaints_bank.csv")
	all = __generate_path_from_train("Consumer_Complaints_all.csv")



class DataSet:
	target = []
	data = []
	target_names = None

	def format(self, file_dir, data_column, category_column):
		with open(file_dir) as csvfile:
			readFile = csv.DictReader(csvfile)

			for row in readFile:
				if row[data_column] != "" and row[data_column] is not None:
					try:
						formatted_str = row[data_column].lower().translate(None, string.punctuation).strip()
						self.data.append(formatted_str)
						self.target.append(row[category_column])
					except Exception as e:
						print e



def train_nb_classifier(file_dir, data_column, category_column="Product"):
	print "starting tfid training"
	with open(file_dir) as csvfile:
		# tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
		readFile = csv.DictReader(csvfile)
		complaint_list = []
		dataset_consumers = DataSet()

		for row in readFile:
			if row[data_column] != "" and row[data_column] is not None:
				try:
					formatted_str = row[data_column].lower().translate(None, string.punctuation).strip()
					complaint_list.append(formatted_str)
					dataset_consumers.data.append(formatted_str)
					dataset_consumers.target.append(row[category_column])
				except Exception as e:
					print e
					print "model was not successfully trained"
					return
		tfidf.fit(complaint_list)
		print "model trained"
		return tfidf

