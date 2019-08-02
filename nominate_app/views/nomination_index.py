from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from nominate_app.models import *
from nominate_app.forms import CommentForm, NominationFilterForm
from django.views.generic.base import View
from IPython import embed
from django.template.loader import render_to_string


# home view for posts. Posts are displayed in a list
class NominationIndexView(View):
	template_name='nominate_app/nomination_index.html'
	context_object_name = 'nomination_list'
	def get(self, request):
		comment_form = CommentForm()
		sort = 'latest'
		if request.GET:
			award_id = request.GET['Awards']
			template_id = request.GET['Templates']
			sort = request.GET['Sort']
			nominations = nomination_filter(request)
			nominate_form = NominationFilterForm(initial={'Awards': award_id, 'Templates': template_id, 'Sort': sort})

		else:
			nominate_form = NominationFilterForm()
			nominations = Nomination.objects.all()

		
		instance_details = get_nomination_instances(nominations, sort)

		return render(request, self.template_name, {'instances': instance_details, 'comment_form': comment_form, 'filter_form': nominate_form})

		
		# return render(request, self.template_name, {self.context_object_name: submitted_nominations, 'filter_form': NominationFilterForm})



def nomination_filter(request):
	award_templates = AwardTemplate.objects.all()
	if request.GET['Templates'] != 'ALL':
		award_templates = AwardTemplate.objects.filter(id=int(request.GET['Templates']))
	
	nominations = Nomination.objects.filter(award_template__in=award_templates)

	return nominations


def get_nomination_instances(nominations, sort):
	if sort == 'latest':
		submitted_instances = NominationInstance.objects.filter(nomination__in=nominations, status=2).order_by('-submitted_at')
	elif sort == 'oldest':
		submitted_instances = NominationInstance.objects.filter(nomination__in=nominations, status=2).order_by('submitted_at')


	instance_details = {}
	for instance in submitted_instances:
		instance_details[instance] = {
			'answers': NominationAnswers.objects.filter(nomination_instance_id=instance, submitted_by_id=instance.user),
			'submitted_at': str(instance.submitted_at),
			'liked': False
		}
		for like in instance.likes.all():
			if like.voter == request.user:
				instance_answers[instance]['liked'] = True

	return instance_details




def nomination_like(request, nomination_instance_id):
	nomination_instance = get_object_or_404(NominationInstance, id=nomination_instance_id)
	like, created = Like.objects.get_or_create(voter=request.user, nomination=nomination_instance)
	if created:
		like.save()
		return JsonResponse({'value':'like'})
	else:
		like.delete()
		return JsonResponse({'value':'unlike'})



class CommentList(View):
	def get(self, request, nomination_instance_id):
		form = CommentForm()
		nomination_instance = get_object_or_404(NominationInstance, id=nomination_instance_id)
		return HttpResponse(render_to_string('nominate_app/nomination_comments.html', {'user': request.user, 'form': form, 'instance': nomination_instance}))


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
		
		return HttpResponse(render_to_string('nominate_app/nomination_comments.html', {'user': request.user, 'form': form, 'instance': nomination_instance}))

	def delete(self, request, nomination_instance_id, comment_id):
		nomination_instance = get_object_or_404(NominationInstance, id=nomintion_instance_id)
		form = CommentForm()
		comment = get_object_or_404(Comment, id=comment_id)
		comment.delete()
		return HttpResponse(render_to_string('nominate_app/nomination_comments.html', {'form': form, 'instance': nomination_instance}))


def comment_remove(request, nomination_instance_id, comment_id):
	nomination_instance = get_object_or_404(NominationInstance, id=nomination_instance_id)
	form = CommentForm()
	comment = get_object_or_404(Comment, id=comment_id)
	comment.delete()
	return HttpResponse(render_to_string('nominate_app/nomination_comments.html', {'user': request.user, 'form': form, 'instance': nomination_instance}))


#Detail view (view post detail)
class NominationDetailView(View):
	template_name = 'nominate_app/nomination_detail.html'
	def get(self, request, award_template_id):
		award_template = AwardTemplate.objects.get(id=award_template_id)
		award = award_template.award
		nominations = Nomination.objects.filter(award_template_id=award_template)
		submitted_instances = NominationInstance.objects.filter(nomination__in=nominations, status=2)
		form = CommentForm()
		instance_answers = {}
		for instance in submitted_instances:
			instance_answers[instance] = {
				'answers': NominationAnswers.objects.filter(nomination_instance_id=instance, submitted_by_id=instance.user),
				'submitted_at': str(instance.submitted_at),
				'liked': False
			}
			for like in instance.likes.all():
				if like.voter == request.user:
					instance_answers[instance]['liked'] = True
		return render(request, self.template_name, {'award': award, 'nomination': award_template, 'instances': instance_answers, 'comment_form': form})
