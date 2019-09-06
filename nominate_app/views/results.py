from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from nominate_app.models import *
from dateutil.relativedelta import relativedelta 
from IPython import embed


def index(request):

    if 'date' in request.GET:
        date = datetime.strptime(request.GET['date'], '%B %Y').date()
    else:
        date = datetime.now().date() - relativedelta(months=1)

    date_field = format(date, '%B %Y')	
    director_comments = DirectorComments.objects.filter(submitted_at__year = date.year, submitted_at__month = date.month)
    approved_submissions = NominationSubmitted.objects.filter(director_comment__in=director_comments, status=2)

    published = []
    unpublished = []
    for submission in approved_submissions:
        s_detail = {
            'object': submission,
            'nomination': submission.nomination,    # to get the start date and end date
            'comment': submission.director_comment.first().comment,
            'image_avail': False,
            'image_path': None
        }

        for question in submission.questions.all():
            if question.attachment_path:
                s_detail['image_avail'] = True
                s_detail['image_path'] = str(question.attachment_path)
        if submission.is_published==True:
            published.append(s_detail)
        else:
            unpublished.append(s_detail)
    return render(request, 'nominate_app/results.html', {'submissions': published, \
		'date': date_field, 'unpublished_submissions':unpublished})

def publish(request, sub_id):
	submission = NominationSubmitted.objects.get(id=sub_id)
	submission.is_published=True
	submission.save()
	return redirect('nominate_app:results')

