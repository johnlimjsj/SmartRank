from django.http import HttpResponse, JsonResponse
from nltkApi.controllers import general_operations
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
	weights = {'urgency': 0.1, 'sentiment': 0.1, 'length': 0.2, 'question': 0.1}
	score = score_dict['urgency'] * weights['urgency'] + score_dict['sentiment'] * weights['sentiment'] + \
			score_dict['length'] * weights['length'] + score_dict['question'] * weights['question']

	return JsonResponse({'score': score})