from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from nominate_app.models import *
from nominate_app.forms import CommentForm, NominationFilterForm
from django.views.generic.base import View
from IPython import embed
import time
from django.template.loader import render_to_string


# home view for posts. Posts are displayed in a list
class NominationIndexView(View):
	template_name='nominate_app/nomination_index.html'
	context_object_name = 'nomination_list'
	def get(self, request):
		comment_form = CommentForm()
		sort = 'latest'
		date_filter = None
		page = request.GET.get('page', 1)

		if 'Awards' in request.GET:
			award_name = request.GET['Awards']
			template_name = request.GET['Templates']
			from_ = request.GET['from_']
			to = request.GET['to']
			sort = request.GET['Sort']
			if from_ and to:
				date_filter = {
					'from': datetime.strptime(from_, '%m/%d/%Y').date(),
					'to': datetime.strptime(to, '%m/%d/%Y').date(),
				}

			nominate_form = NominationFilterForm(initial={'Awards': award_name, 'Templates': template_name, 'Sort': sort, 'from_': from_, 'to': to})
			submissions =  submission_filter(award_name, template_name, date_filter, sort)

		else:
			nominate_form = NominationFilterForm()
			submissions = NominationSubmitted.objects.all()

		paginator = Paginator(submissions, 10)
		submissions = paginator.page(page)

		instances = []
		for submission in submissions:
			instances.append(nomination_instance_detail(submission, request.user))


		return render(request, self.template_name, {'instances': instances, 'comment_form': comment_form, 'filter_form': nominate_form})



def submission_filter(award_name, template_name, date_filter, sort):
	submissions = NominationSubmitted.objects.all()
	if award_name != 'ALL':
		submissions = submissions.filter(award_name=award_name)

	if template_name != 'ALL':
		submissions = submissions.filter(template_name=template_name)

	if date_filter:
		submissions = submissions.filter(submitted_at__gte=date_filter['from'], submitted_at__lte=date_filter['to'])

	if sort == 'latest':
		submissions = submissions.order_by('-submitted_at')
	elif sort == 'oldest':
		submissions = submissions.order_by('submitted_at')

	return submissions


def nomination_instance_detail(submission, requested_user):
	likes_count = submission.likes.count()
	comments_count = submission.comments.count()
	is_liked = Like.objects.filter(submission=submission, voter_id=requested_user).exists()
	instance={
		'submission': submission,
		'qa': QuestionAnswers.objects.filter(nomination_submitted=submission),
		'detail':{
			'is_liked': is_liked,
			'likes_count': likes_count - 1 if is_liked else likes_count,
			'comments_count': comments_count
		}
	}
	
	return instance


# view for single nomination instance
def nomination_instance_post(request, nomination_submittion_id):
	submission = NominationSubmitted.objects.get(id=nomination_submittion_id)
	instance = nomination_instance_detail(submission, request.user)
	comment_form = CommentForm()
	return render(request, 'nominate_app/nomination_instance.html', {'instance': instance, 'comment_form':comment_form})

# For Like and unlike in nomination instances
def nomination_like(request, nomination_submittion_id):
	nomination_submission = get_object_or_404(NominationSubmitted, id=nomination_submittion_id)
	like, created = Like.objects.get_or_create(voter=request.user, submission=nomination_submission) 
	if created:
		like.save()
		return JsonResponse({'value':'like'})
	else:
		like.delete()
		return JsonResponse({'value':'unlike'})

def nomination_liked_people(request, nomination_submittion_id):
	nomination_submission = get_object_or_404(NominationSubmitted, id=nomination_submittion_id)
	likes = nomination_submission.likes.all()
	liked_people = []
	for like in likes:
		liked_people.append(like.voter.email)

	return JsonResponse({'liked_people': liked_people})


# For comment resource of nomination instance
class CommentList(View):
	def get(self, request, nomination_submittion_id):
		form = CommentForm()
		page = request.GET.get('page', 1)
		nomination_submission = get_object_or_404(NominationSubmitted, id=nomination_submittion_id)
		comments = nomination_submission.comments.order_by('-created_date')

		paginator = Paginator(comments, 3)

		try:
			comments = paginator.page(page)
		except PageNotAnInteger:
			comments = paginator.page(1)
		except EmptyPage:
			comments = []

		comments.object_list = comments.object_list[::-1]

		return HttpResponse(render_to_string('nominate_app/nomination_comments.html', {'user': request.user, 'form': form, 'instance': nomination_submission, 'comments': comments}))


	def post(self, request, nomination_submittion_id):
		nomination_submission = get_object_or_404(NominationSubmitted, id=nomination_submittion_id)
		form = CommentForm()
		form = CommentForm(request.POST)
		if form.is_valid():
		  comment = form.save(commit=False)
		comment = Comment()
		comment.submission = nomination_submission
		comment.text = request.POST['comment']
		comment.author = request.user
		comment.save()

		comments = []
		comments.append(comment)

		return HttpResponse(render_to_string('nominate_app/nomination_comments.html', {'user': request.user, 'form': form, 'instance': nomination_submission, 'comments': comments}))


def comment_remove(request, nomination_submittion_id, comment_id):
	form = CommentForm()
	comment = get_object_or_404(Comment, id=comment_id)
	if comment:
		comment.delete()
		return JsonResponse({'status': "deleted"})

	return JsonResponse({'status': "error"})

