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
			nominations = nomination_filter(award_id, template_id)
			nominate_form = NominationFilterForm(initial={'Awards': award_id, 'Templates': template_id, 'Sort': sort})

		else:
			nominate_form = NominationFilterForm()
			nominations = Nomination.objects.all()

		instance_details = {}
		instances = nomination_sort(nominations, sort)
		for instance in instances:
			instance_details[instance] = nomination_instance_detail(instance, request.user)

		return render(request, self.template_name, {'instances': instance_details, 'comment_form': comment_form, 'filter_form': nominate_form})



def nomination_filter(award_id, template_id):
	awards = Awards.objects.all() if award_id == 'ALL' else Awards.objects.filter(id=int(award_id))
	award_templates = AwardTemplate.objects.filter(award__in=awards) if template_id =='ALL' else AwardTemplate.objects.filter(award__in=awards, id=int(template_id))
	nominations = Nomination.objects.filter(award_template__in=award_templates)

	return nominations


def nomination_sort(nominations, sort):
	if sort == 'latest':
		sorted_instances = NominationInstance.objects.filter(nomination__in=nominations, status=2).order_by('-submitted_at')
	elif sort == 'oldest':
		sorted_instances = NominationInstance.objects.filter(nomination__in=nominations, status=2).order_by('submitted_at')

	return sorted_instances
	

def nomination_instance_detail(instance, requested_user):
	instance_detail = {
		'answers': NominationAnswers.objects.filter(nomination_instance_id=instance, submitted_by_id=instance.user),
		'submitted_at': str(instance.submitted_at),
		'liked': False
	}
	for like in instance.likes.all():
		if like.voter == requested_user:
			instance_detail['liked'] = True

	return instance_detail



# view for single nomination instance
def nomination_instance_post(request, nomination_instance_id):
	instance = NominationInstance.objects.get(id=nomination_instance_id)
	instance_detail = nomination_instance_detail(instance, request.user)
	comment_form = CommentForm()
	embed()
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


# For comment resource of nomination instance
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


