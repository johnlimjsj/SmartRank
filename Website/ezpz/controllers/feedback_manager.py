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
	fb_sorted = Feedback.objects.all()
	feedback_list = []
	for fb in fb_sorted:
		feedback = fb.feedback
		date_created = fb.date_created
		score_dict = general_operations._get_priority_score_dict(feedback, date_created)
		score = general_operations._get_priority_score(score_dict)
		fb.priority = score
		fb.save()
		feedback_list.append({'feedback': feedback, 'score': score})

	sorted_fb_list = sorted(feedback_list, key=itemgetter('score'), reverse=True)

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
