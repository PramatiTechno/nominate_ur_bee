from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from nominate_app.models import *
from django.db.models import Avg
from django.views.generic.base import View
from nominate_app.utils import group_required
from braces.views import GroupRequiredMixin
from IPython import embed


@group_required('Technical Jury Member', raise_exception=True)
def index(request):
	statuses = ('Submitted', 'Reviewed')
	status = request.GET['status'] if 'status' in request.GET else statuses[0]

	status_code = 0 if status == 'Submitted' else 1
	submissions = NominationSubmitted.objects.filter(status=status_code)
	return render(request, 'nominate_app/nomination_review/index.html', {'statuses': statuses, 'c_status':status, 'submissions': submissions}) 


@method_decorator(csrf_exempt, name='dispatch')
class nomination_rating(GroupRequiredMixin, View):

	group_required = u"Technical Jury Member"
	
	def get(self, request, nomination_submitted_id):
		submission = NominationSubmitted.objects.get(id=nomination_submitted_id)
		created = NominationRating.objects.filter(user=request.user, submission=submission).exists()

		total_rating = submission.ratings.count()
		avg_rating = NominationRating.objects.filter(submission=submission).aggregate(Avg('rating'))['rating__avg'] if total_rating > 0 else 0.0 
		if not created:
			return render(request, 'nominate_app/nomination_review/new.html', {'submission': submission, 'average_rating': avg_rating, 'total_rating': total_rating})

		nomination_rating = NominationRating.objects.get(user=request.user, submission=submission)
		return render(request, 'nominate_app/nomination_review/show.html', {'submission': submission, 'rating': nomination_rating.rating, 'review': nomination_rating.review, 'average_rating': avg_rating, 'total_rating': total_rating})		


	def post(self, request, nomination_submitted_id):
		submission = NominationSubmitted.objects.get(id=nomination_submitted_id)
		rating = request.POST['rating']
		review = request.POST['review']
		nomination_rating, created = NominationRating.objects.get_or_create(user=request.user, submission=submission)
		if created:
			if rating != 0 and review != '':
				nomination_rating.rating = rating
				nomination_rating.review = review
				submission.status = 1                # status code for reviewed
				nomination_rating.save()
				submission.save()

				avg_rating = NominationRating.objects.filter(submission=submission).aggregate(Avg('rating'))['rating__avg']
				total_rating = submission.ratings.count()
				return redirect('nominate_app:nomination_review_rating', nomination_submitted_id=submission.id)
