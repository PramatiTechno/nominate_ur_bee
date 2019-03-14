from django.shortcuts import render, redirect 
from django.forms import modelformset_factory, inlineformset_factory
from nominate_app.forms import NominationAnswersForm
from nominate_app.models import NominationPeriod, AwardTemplate, NominationPlan, NominationInstance, NominationSubmitter, User, Questions, NominationAnswers
from django.http import HttpResponse
from django.contrib import messages
import json
import os
from django.conf import settings

# Create your views here.

def manager_nominate_index(request):
  current_user = User.objects.get(id=request.user.id)

  todo_nomination_chains = NominationSubmitter.objects.filter(nomination_instance__status='new', reviewer_id=current_user.id).select_related('nomination_instance').order_by('id')

  done_nominations = NominationSubmitter.objects.filter(nomination_instance__status='nomination_submitted',reviewer_id=current_user.id).select_related('nomination_instance').order_by('id')

  return render(request, 'nominate_app/manager_nominate_index.html', {'todo_nomination_chains':todo_nomination_chains, 'done_nominations':done_nominations })


def create_nomination(request,chain_id):
  answers_form = NominationAnswersForm(instance=NominationAnswers())
  nomination_chain = NominationSubmitter.objects.get(id=chain_id)
  nomination_instance = nomination_chain.nomination_instance
  nomination_template = nomination_instance.award_template
  questions = Questions.objects.filter(award_template = nomination_template).order_by('id')

  if request.method == 'POST':
    new_form = request.POST.copy()
    dict_new_form = dict(new_form)

    # This code to be refactored. Multiple answer records submit

    ques_answers_dict = {k.split('_')[0]: v for k, v in dict_new_form.items() if k.endswith('answer')}
    edit_new_form = new_form.copy()
    for key in edit_new_form.keys():
      if key.endswith('answer'):
        new_form.pop(key)

    ans_obj_List = []
    for qid,answer in ques_answers_dict.items():
      ans_form1 = new_form.copy()
      ans_form1['question'] = qid
      ans_form1['answer_text'] = answer
      ans_form1['nomination_chain'] = chain_id
      # current_user = request.user
      # ans_form1['submitted_by'] = current_user.id
      ans_form1['submitted_by'] = 1
      ans_obj_List.append(ans_form1)

   
    for ans_obj in ans_obj_List:
      qid = ans_obj['question']
      files = request.FILES.getlist(qid+'_attachment_path')

      if files:
        nn = request.FILES.copy()
        attachment_path = nn[qid+'_attachment_path']
        request.FILES.pop(qid+'_attachment_path')
        request.FILES['attachment_path'] = attachment_path
        answers_form = NominationAnswersForm(ans_obj, request.FILES)
      else:
        answers_form = NominationAnswersForm(ans_obj)

      if answers_form.is_valid():
        created_answer = answers_form.save()

    nom_inst = NominationInstance.objects.filter(id= nomination_instance.id)
    nom_inst.update(status='nomination_submitted')

    messages.success(request, 'Nomination submitted successfully.')
    return redirect('nominate_app:manager_nominate_index')

  return render(request, 'nominate_app/create_nomination.html', {'answers_form':answers_form,'nomination_chain':nomination_chain,'nomination_instance':nomination_instance, 'nomination_template':nomination_template, 'questions':questions })

def view_nomination(request,chain_id):
  answers_form = NominationAnswersForm(instance=NominationAnswers())
  nomination_chain = NominationSubmitter.objects.get(id=chain_id)
  nomination_instance = nomination_chain.nomination_instance
  nomination_template = nomination_instance.award_template
  nom_answers = NominationAnswers.objects.filter(nomination_instance_id =nomination_instance,award_template_id=nomination_template).order_by('id')

  return render(request, 'nominate_app/view_nomination.html', {'answers_form':answers_form,'nomination_chain':nomination_chain, 'nomination_template':nomination_template, 'nomination_answers': nom_answers })