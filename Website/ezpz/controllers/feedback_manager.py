from django.http import HttpResponse, JsonResponse
from nltkApi.controllers import general_operations
from django.views.decorators.http import require_POST, require_GET
from ezpz.models import Feedback
import json
from operator import itemgetter

@require_POST
def store_feedback(request):
	data = json.loads(request.body)
	feedback = data['feedback']
	Feedback.create(feedback=feedback)

	return JsonResponse({'status': "success"})

@require_GET
def get_sorted_feedback(request):

	def get_manpower(score):
		manpower_list = [
			{'name': 'Lee Hsien Loong', 'min': 0.8, 'max': 1.0},
			{'name': 'Trump', 'min': 0.75, 'max': 0.8},
			{'name': 'Teo Chee Hean', 'min': 0.7, 'max': 0.75},
			{'name': 'Goh Chok Tong', 'min': 0.65, 'max': 0.7},
			{'name': 'Daniel Seetoh', 'min': 0.6, 'max': 0.65},
			{'name': 'John Lim', 'min': 0.5, 'max': 0.6},
			{'name': 'Nisha Srinidhi', 'min': 0.4, 'max': 0.5},
			{'name': 'Nikhil Srinidhi', 'min': 0.3, 'max': 0.4},
			{'name': 'Joshua Seetoh', 'min': 0.2, 'max': 0.3},
			{'name': 'Kwan Yew Lee', 'min': 0.15, 'max': 0.2},
			{'name': 'Benjamin Lee', 'min': 0.1, 'max': 0.15},
		]

		for man in manpower_list:
			if score >= man['min'] and score < man['max']:
				return man['name']

	fb_sorted = Feedback.objects.all()
	feedback_list = []
	for fb in fb_sorted:
		feedback = fb.feedback
		date_created = fb.date_created
		score_dict = general_operations._get_priority_score_dict(feedback, date_created)
		score = general_operations._get_priority_score(score_dict)
		fb.priority = score
		fb.save()
		feedback_list.append({'feedback': feedback, 'score': score, 'person': get_manpower(score)})

	sorted_fb_list = sorted(feedback_list, key=itemgetter('score'), reverse=True)

	# print sorted_fb_list

	return JsonResponse({'feedback': sorted_fb_list})


@require_GET
def get_sorted_feedback_dict(request):
	fb_sorted = Feedback.objects.all()
	feedback_list = []
	for fb in fb_sorted:
		feedback = fb.feedback
		date_created = fb.date_created
		score_dict = general_operations._get_priority_score_dict(feedback, date_created)
		score = general_operations._get_priority_score(score_dict)
		fb.priority = score
		fb.save()
		feedback_list.append({'feedback': feedback, 'score': score, 'score_dict': score_dict})

	sorted_fb_list = sorted(feedback_list, key=itemgetter('score'), reverse=True)

	return JsonResponse({'feedback': sorted_fb_list})
