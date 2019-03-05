from django.shortcuts import render, redirect 
from django.forms import modelformset_factory, inlineformset_factory
from nominate_app.forms import NominationAnswersForm, AnswerAttachmentForm
from nominate_app.models import NominationPeriod, AwardTemplate, NominationPlan, NominationInstance, NominationChain, User, Questions, AnswerAttachment, NominationAnswers
from django.http import HttpResponse
from django.contrib import messages
import json

# Create your views here.

def manager_nominate_index(request):
  # current_user = request.user
  current_user = User.objects.get(id=1)
  nomination_chain = NominationChain.objects.filter(nomination_instance__status='new').filter(reviewer_id=current_user.id).select_related('nomination_instance').first()
  nomination_instance = nomination_chain.nomination_instance
  nomination_template = nomination_instance.award_template

  return render(request, 'nominate_app/manager_nominate_index.html', {'nomination_chain':nomination_chain,'nomination_instance':nomination_instance, 'nomination_template':nomination_template })


def create_nomination(request,chain_id):
  answers_form = NominationAnswersForm(instance=NominationAnswers())
  answer_attachment_form = AnswerAttachmentForm()
  nomination_chain = NominationChain.objects.get(id=chain_id)
  nomination_instance = nomination_chain.nomination_instance
  nomination_template = nomination_instance.award_template
  questions = Questions.objects.filter(award_template = nomination_template)

  if request.method == 'POST':
    answers_form = NominationAnswersForm(request.POST)
    answer_attachment_form = AnswerAttachmentForm(request.POST, request.FILES)
    files = request.FILES.getlist('attachment_path')
    
    if answers_form.is_valid():
      created_answer = answers_form.save()
      for f in files:
        file_instance = AnswerAttachment(file=f, answer_id=created_answer)
        file_instance.save()

      messages.success(request, 'Nomination submitted successfully.')
      return render(request, 'nominate_app/manager_nominate_index.html', {'nomination_chain':nomination_chain,'nomination_instance':nomination_instance, 'nomination_template':nomination_template })
  return render(request, 'nominate_app/create_nomination.html', {'answers_form':answers_form,'answer_attachment_form':answer_attachment_form,'nomination_chain':nomination_chain,'nomination_instance':nomination_instance, 'nomination_template':nomination_template, 'questions':questions })