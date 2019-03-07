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
    new_form = request.POST.copy()

    dict_new_form = dict(new_form)
    ques_answers_dict = {k.split('_')[0]: v for k, v in dict_new_form.items() if k.endswith('answer')}

    edit_new_form = new_form.copy()
    for key in edit_new_form.keys():
      if key.endswith('answer'):
        new_form.pop(key)

    ans_obj_List = []
    for key,value in ques_answers_dict.items():
      ans_form1 = new_form.copy()
      ans_form1['question_id'] = key
      ans_form1['answer_text'] = value
      ans_form1['nomination_chain'] = chain_id
      # current_user = request.user
      # ans_form1['submitted_by'] = current_user.id
      ans_form1['submitted_by'] = 1
      ans_obj_List.append(ans_form1)

    for ans_obj in ans_obj_List:
      answers_form = NominationAnswersForm(ans_obj)
      if answers_form.is_valid():
        created_answer = answers_form.save()
    # answer_attachment_form = AnswerAttachmentForm(request.POST, request.FILES)
    # files = request.FILES.getlist('attachment_path')
    
    # if answers_form.is_valid():
    #   created_answer = answers_form.save()
    #   for f in files:
    #     file_instance = AnswerAttachment(file=f, answer_id=created_answer)
    #     file_instance.save()

    messages.success(request, 'Nomination submitted successfully.')
    return render(request, 'nominate_app/manager_nominate_index.html', {'nomination_chain':nomination_chain,'nomination_instance':nomination_instance, 'nomination_template':nomination_template })
  return render(request, 'nominate_app/create_nomination.html', {'answers_form':answers_form,'answer_attachment_form':answer_attachment_form,'nomination_chain':nomination_chain,'nomination_instance':nomination_instance, 'nomination_template':nomination_template, 'questions':questions })