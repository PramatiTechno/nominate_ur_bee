from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from nominate_app.models import *
from dateutil.relativedelta import relativedelta 
from IPython import embed


def index(request):

	if 'date' in request.GET:
		date = datetime.strptime(request.GET['date'], '%B %Y').date()
		date_field = format(date, '%B %Y')
		director_comments = DirectorComments.objects.filter(submitted_at__year = date.year, submitted_at__month = date.month)
		approved_submissions = NominationSubmitted.objects.filter(director_comment__in=director_comments, status=2)

	else:
		last_month = datetime.now().date() - relativedelta(months=1)
		date_field = format(last_month, '%B %Y')
		director_comments = DirectorComments.objects.filter(submitted_at__year = last_month.year, submitted_at__month = last_month.month)
		approved_submissions = NominationSubmitted.objects.filter(director_comment__in=director_comments, status=2)


	submissions = []
	for submission in approved_submissions:
		s_detail = {
			'object': submission,
			'nomination': submission.nomination,    # to get the start date and end date
			'comment': submission.director_comment.first().comment

		}
		submissions.append(s_detail)

	return render(request, 'nominate_app/results.html', {'submissions': submissions, 'date': date_field}) 
