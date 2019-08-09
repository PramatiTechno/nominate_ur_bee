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
			award_id = request.GET['Awards']
			template_id = request.GET['Templates']
			from_ = request.GET['from_']
			to = request.GET['to']
			sort = request.GET['Sort']
			nominations = nomination_filter(award_id, template_id)
			nominate_form = NominationFilterForm(initial={'Awards': award_id, 'Templates': template_id, 'Sort': sort, 'from_': from_, 'to': to})

			if from_ and to:
				date_filter = {
					'from': datetime.strptime(from_, '%m/%d/%Y').date(),
					'to': datetime.strptime(to, '%m/%d/%Y').date(),
				}

		else:
			nominate_form = NominationFilterForm()
			nominations = Nomination.objects.all()


		instance_details = []
		instances = instance_filter_sort(nominations, sort, date_filter)

		for instance in instances:
			instance_details.append({
				'instance': instance,
				'detail': nomination_instance_detail(instance, request.user)
				})

		paginator = Paginator(instance_details, 10)
		instance_details = paginator.page(page)

		return render(request, self.template_name, {'instances': instance_details, 'comment_form': comment_form, 'filter_form': nominate_form})



def nomination_filter(award_id, template_id):
	awards = Awards.objects.all() if award_id == 'ALL' else Awards.objects.filter(id=int(award_id))
	award_templates = AwardTemplate.objects.filter(award__in=awards) if template_id =='ALL' else AwardTemplate.objects.filter(award__in=awards, id=int(template_id))
	nominations = Nomination.objects.filter(award_template__in=award_templates)

	return nominations


def instance_filter_sort(nominations, sort, date_filter):
	if date_filter:
		instances = NominationInstance.objects.filter(nomination__in=nominations, status=2, submitted_at__gte=date_filter['from'], submitted_at__lte=date_filter['to'])
	else:
		instances = NominationInstance.objects.filter(nomination__in=nominations, status=2)

	if sort == 'latest':
		sorted_instances = instances.order_by('-submitted_at')
	elif sort == 'oldest':
		sorted_instances = instances.order_by('submitted_at')

	return sorted_instances
	

def nomination_instance_detail(instance, requested_user):
	likes_count = instance.likes.count()
	comments_count = instance.comments.count()
	instance_detail = {
		'answers': NominationAnswers.objects.filter(nomination_instance_id=instance, submitted_by_id=instance.user),
		'submitted_at': str(instance.submitted_at),
		'is_liked': False,
		'likes_count': likes_count - 1 if likes_count > 0 else 0,
		'comments_count': comments_count
	}
	for like in instance.likes.all():
		if like.voter == requested_user:
			instance_detail['is_liked'] = True

	return instance_detail



# view for single nomination instance
def nomination_instance_post(request, nomination_instance_id):
	instance = NominationInstance.objects.get(id=nomination_instance_id)
	instance_detail = nomination_instance_detail(instance, request.user)
	comment_form = CommentForm()
	return render(request, 'nominate_app/nomination_instance.html', {'instance': instance, 'detail': instance_detail, 'comment_form':comment_form})

# For Like and unlike in nomination instances
def nomination_like(request, nomination_instance_id):
	nomination_instance = get_object_or_404(NominationInstance, id=nomination_instance_id)
	like, created = Like.objects.get_or_create(voter=request.user, nomination=nomination_instance) 
	if created:
		like.save()
		return JsonResponse({'value':'like'})
	else:
		like.delete()
		return JsonResponse({'value':'unlike'})

def nomination_liked_people(request, nomination_instance_id):
	nomination_instance = get_object_or_404(NominationInstance, id=nomination_instance_id)
	likes = nomination_instance.likes.all()
	liked_people = []
	for like in likes:
		liked_people.append(like.voter.email)

	return JsonResponse({'liked_people': liked_people})


# For comment resource of nomination instance
class CommentList(View):
	def get(self, request, nomination_instance_id):
		form = CommentForm()
		page = request.GET.get('page', 1)
		nomination_instance = get_object_or_404(NominationInstance, id=nomination_instance_id)
		comments = nomination_instance.comments.order_by('-created_date')

		paginator = Paginator(comments, 3)

		try:
			comments = paginator.page(page)
		except PageNotAnInteger:
			comments = paginator.page(1)
		except EmptyPage:
			comments = []

		comments.object_list = comments.object_list[::-1]

		return HttpResponse(render_to_string('nominate_app/nomination_comments.html', {'user': request.user, 'form': form, 'instance': nomination_instance, 'comments': comments}))


	def post(self, request, nomination_instance_id):
		nomination_instance = get_object_or_404(NominationInstance, id=nomination_instance_id)
		form = CommentForm()
		form = CommentForm(request.POST)
		if form.is_valid():
		  comment = form.save(commit=False)
		comment = Comment()
		comment.nomination = nomination_instance
		comment.text = request.POST['comment']
		comment.author = request.user
		comment.save()

		comments = []
		comments.append(comment)

		return HttpResponse(render_to_string('nominate_app/nomination_comments.html', {'user': request.user, 'form': form, 'instance': nomination_instance, 'comments': comments}))


def comment_remove(request, nomination_instance_id, comment_id):
	nomination_instance = get_object_or_404(NominationInstance, id=nomination_instance_id)
	form = CommentForm()
	comment = get_object_or_404(Comment, id=comment_id)
	if comment:
		comment.delete()
		return JsonResponse({'status': "deleted"})

	return JsonResponse({'status': "error"})

