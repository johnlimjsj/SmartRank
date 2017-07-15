import csv
import string
import os

DATA_ROOT_PATH = "ezpz/static/ezpz/data/"
TRAINING_DATA_ROOT = DATA_ROOT_PATH + "training_data/"
TEST_DATA_ROOT = DATA_ROOT_PATH + "test_data/"

FEEDBACK_DATA_PATH = TRAINING_DATA_ROOT + "UrgencyDataset.csv"
QUESTIONS_DATA_PATH = TRAINING_DATA_ROOT + "QuestionsDataset.csv"

class ConsumerComplaints:

	def __generate_path_from_train(fileName):
		return TRAINING_DATA_ROOT + fileName

	bank = __generate_path_from_train("Consumer_Complaints_bank.csv")
	all = __generate_path_from_train("Consumer_Complaints_all.csv")




class DataSet:
	target = []
	data = []
	target_names = None

	def format_list(self, file_dir, data_column):
		with open(file_dir) as csvfile:
			readFile = csv.DictReader(csvfile)
			for row in readFile:
				try:
					if row[data_column] != "" and row[data_column] is not None:

						formatted_str = row[data_column].lower().translate(None, string.punctuation).strip()
						self.data.append(formatted_str)
				except Exception as e:
					print e


	def format(self, file_dir, data_column, category_column):
		print "trying to open"
		with open(file_dir) as csvfile:
			print "opened"
			readFile = csv.DictReader(csvfile)
			print "trying to read"
			for row in readFile:

				if row[data_column] != "" and row[data_column] is not None:
					try:
						formatted_str = row[data_column].lower().translate(None, string.punctuation).strip()
						self.data.append(formatted_str)
						self.target.append(row[category_column])
					except Exception as e:
						print "exception found"




