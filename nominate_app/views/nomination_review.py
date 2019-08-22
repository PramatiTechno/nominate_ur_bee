from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from nominate_app.models import *
from django.db.models import Avg
from django.views.generic.base import View
from nominate_app.utils import group_required
from braces.views import GroupRequiredMixin
from django.utils import timezone
from django.contrib import messages
from IPython import embed


def index(request):
	statuses = ('To be Submitted', 'Reviewed')
	status = request.GET['status'] if 'status' in request.GET else statuses[0]

	if status == 'To be Submitted':
		submissions = NominationSubmitted.objects.filter(status=0) # status for submitted
	else:
		submissions = NominationSubmitted.objects.filter(ratings__user=request.user)

	return render(request, 'nominate_app/nomination_review/index.html', {'statuses': statuses, 'c_status':status, 'submissions': submissions}) 


@method_decorator(csrf_exempt, name='dispatch')
class nomination_rating(GroupRequiredMixin, View):

	group_required = u"Technical Jury Member"
	
	def get(self, request, nomination_submitted_id):
		submission = NominationSubmitted.objects.get(id=nomination_submitted_id)
		created = NominationRating.objects.filter(user_id=request.user.id, submission=submission).exists()

		total_rating = submission.ratings.count()
		avg_rating = NominationRating.objects.filter(submission=submission).aggregate(Avg('rating'))['rating__avg'] if total_rating > 0 else 0.0 
		if not created:
			return render(request, 'nominate_app/nomination_review/new.html', {'submission': submission, 'average_rating': avg_rating, 'total_rating': total_rating})

		nomination_rating = NominationRating.objects.get(user_id=request.user.id, submission=submission)
		return render(request, 'nominate_app/nomination_review/show.html', {'submission': submission, 'rating': nomination_rating.rating, 'review': nomination_rating.review, 'average_rating': avg_rating, 'total_rating': total_rating})		


	def post(self, request, nomination_submitted_id):
		submission = NominationSubmitted.objects.get(id=nomination_submitted_id)
		rating = request.POST['rating']
		review = request.POST['review']
		created = NominationRating.objects.filter(user_id=request.user.id, submission=submission).exists()
		if not created:
			if rating != '0.0' and review != '':
				nomination_rating = NominationRating(user=request.user, submission=submission, rating=rating, review=review)
				submission.status = 1                # status code for reviewed
				submission.updated_at = timezone.now()
				nomination_rating.save()
				submission.save()
				return redirect('nominate_app:nomination_review_rating', nomination_submitted_id=submission.id)

			else:
				messages.error(request, "ratings and reviews can't be blank")
				total_rating = submission.ratings.count()
				avg_rating = NominationRating.objects.filter(submission=submission).aggregate(Avg('rating'))['rating__avg'] if total_rating > 0 else 0.0
				return render(request, 'nominate_app/nomination_review/new.html', {'submission': submission, 'average_rating': avg_rating, 'total_rating': total_rating})