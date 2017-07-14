from django.http import HttpResponse, JsonResponse
from nltkApi.controllers import general_operations
from ezpz.models import Feedback
import json


def get_priority_score_dict(request):
	data = json.loads(request.body)
	feedback = data['feedback']
	score_dict = general_operations._get_priority_score_dict(feedback)
	return JsonResponse(score_dict)


def get_priority_score(request):
	data = json.loads(request.body)
	feedback = data['feedback']
	score_dict = general_operations._get_priority_score_dict(feedback)
	score = general_operations._get_priority_score(score_dict)

	# populating the database
	Feedback.create(feedback=feedback, priority=score)

	#return the score as json
	return JsonResponse({'score': score})


