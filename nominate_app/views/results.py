from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from nominate_app.models import *
from IPython import embed


def index(request):

	approved_submissions = NominationSubmitted.objects.all()
	embed()
	if 'date' in request.GET:
		date = datetime.strptime(request.GET['date'], '%B %Y').date()
		# director_comments = DirectorComment.objects.filter(submitted_at__year = month.year, submitted_at__month = month.month)
		# approved_submissions = NominationSubmitted.objects.filter(director_comment__in=director_comments, status=2)


	submissions = []
	for submission in approved_submissions:
		s_detail = {
			'object': submission,
			'nomination': submission.nomination,    # to get the start date and end date
			'comments': None #submission.director_comment.comment

		}
		submissions.append(s_detail)

	return render(request, 'nominate_app/results.html', {'submissions': submissions}) 
