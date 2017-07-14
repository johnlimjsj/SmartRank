# -*- coding: utf-8 -*-
import json
from django.test import TestCase, Client


class SmartRankTests(TestCase):
	def test_feedback(self):

		data = {'feedback': "user input data"}
		c = Client()
		response = c.post(
			path='/get-priority/',
			data=json.dumps(data),
			content_type="application/json"
		)
		print response
		json_response = json.loads(response.content)
		# print json_response

		# incoming_text = request.POST.get('text')
