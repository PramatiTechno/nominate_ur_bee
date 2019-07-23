from django.shortcuts import render, redirect, get_object_or_404
from nominate_app.models import *
from django.views.generic.base import View
from IPython import embed

# home view for posts. Posts are displayed in a list
class NominationIndexView(View):
	template_name='nominate_app/nomination_index.html'
	context_object_name = 'nomination_list'
	def get(self, request):
		submitted_instances = NominationInstance.objects.filter(status='nomination_submitted')
		submitted_nominations = AwardTemplate.objects.filter(id__in=submitted_instances)
		return render(request, self.template_name, {self.context_object_name: submitted_nominations})

# def get_nomination_index(request):
# 	submitted_instances = NominationInstance.objects.filter(status='new')
# 	submitted_nominations = AwardTemplate.objects.filter(id__in=submitted_instances)
# 	return render(request, 'nominate_app/nomination_index.html', {'nomination_list': submitted_nominations})


#Detail view (view post detail)
class NominationDetailView(View):
	template_name = 'nominate_app/nomination_detail.html'
	def get(self, request, award_template_id):
		award_template = AwardTemplate.objects.get(id=award_template_id)
		award = award_template.award
		submitted_instances = NominationInstance.objects.filter(award_template_id=award_template, status='nomination_submitted')
		instance_answers = {}
		for instance in submitted_instances:
			instance_answers[instance] = {
				'answers': NominationAnswers.objects.filter(nomination_instance_id=instance, submitted_by_id=instance.user),
				'submitted_at': str(instance.nominationsubmitter_set.values().filter(reviewer_id=instance.user)[0]['reviewed_at'])
			}
		return render(request, self.template_name, {'award': award, 'nomination': award_template, 'instances': instance_answers})

