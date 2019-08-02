from django.shortcuts import render, redirect 
from django.forms import modelformset_factory, inlineformset_factory
from nominate_app.forms import NominationAnswersForm
from nominate_app.models import Nomination,NominationPeriod, AwardTemplate, NominationInstance, User, Questions, NominationAnswers
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
import json
from django.utils import timezone
import os
from django.conf import settings
from datetime import datetime
from IPython import embed

def index(request,nomination_id):
  if request.method == 'POST':  
    answers_form = NominationAnswersForm(instance=NominationAnswers())
    nomination = Nomination.objects.get(id=nomination_id)
    nomination_instance = NominationInstance.objects.get_or_create(nomination=nomination,user=request.user)[0]
    nomination_template = nomination.award_template
    questions = Questions.objects.filter(award_template = nomination_template,group=nomination.group).order_by('id')
    new_form = request.POST.copy()
    dict_new_form = dict(new_form)
    ques_answers_dict = {}
    for k, v in dict_new_form.items():
      if k.endswith('answer_option'):
        ques_answers_dict[k.split('_')[0]] = {'value':v, 'option': True}  
      elif k.endswith('answer'):
          ques_answers_dict[k.split('_')[0]] = {'value':v, 'option': False} 
    
    edit_new_form = new_form.copy()
    for key in edit_new_form.keys():
      if key.endswith('answer'):
        new_form.pop(key)

    if request.method == 'POST':
      ans_obj_List = []
      for qid,answer in ques_answers_dict.items():
        ans_form1 = new_form.copy()
        ans_form1['question'] = qid
        ans_form1['answer_text'] = answer['value']
        ans_form1['option'] = answer['option']
        ans_form1['submitted_by'] = 1
        ans_obj_List.append(ans_form1)

      for ans_obj in ans_obj_List:
        qid = ans_obj['question']
        files = request.FILES.getlist(qid+'_attachment_path')
      if answers_form.is_valid():
        created_answer = answers_form.save()

        if files:
          nn = request.FILES.copy()
          attachment_path = nn[qid+'_attachment_path']
          request.FILES.pop(qid+'_attachment_path')
          request.FILES['attachment_path'] = attachment_path
          
          answers_form = NominationAnswersForm(ans_obj, request.FILES)
        else:
          answers_form = NominationAnswersForm(ans_obj)
      nomination_answers = NominationAnswers.objects.filter(nomination_instance_id=nomination_instance.id)
      for ans in ans_obj_List:
        try:
          condition1 = Q(nomination_instance_id=nomination_instance.id)
          condition2 = Q(question_id=ans['question'])
          na = NominationAnswers.objects.get(condition1 & condition2)
          na.answer_text = ans['answer_text'][0]
          na.answer_option = ans['option']
          na.save()
        except Exception as e:
          print(e)
          na = NominationAnswers(answer_option=ans['option'], answer_text=ans['answer_text'][0],nomination_instance_id=nomination_instance.id, uploaded_at=timezone.now(), award_template_id=ans['award_template'],question_id=ans['question'], submitted_by=request.user)
          na.save()

      # This code to be refactored. Multiple answer records submit
      if request.POST['action'] == 'save':
        nomination_instance.status = 1
        nomination_instance.save()
        messages.success(request, 'Nomination saved successfully.')
      elif request.POST['action'] == 'submit':
        nomination_instance.status = 2
        nomination_instance.submitted_at = datetime.now()
        nomination_instance.save()
        messages.success(request, 'Nomination submitted successfully.')
      return redirect('nominate_app:nominations')

def new(request,nomination_id):
  answers_form = NominationAnswersForm(instance=NominationAnswers())
  nomination = Nomination.objects.get(id=nomination_id)
  nomination_instance = NominationInstance(nomination=nomination)
  
  nomination_template = nomination.award_template
  questions = Questions.objects.filter(award_template = nomination_template,group=nomination.group).order_by('id')
  new_form = request.POST.copy()
  dict_new_form = dict(new_form)
  ques_answers_dict = {}
  for k, v in dict_new_form.items():
    if k.endswith('answer_option'):
      ques_answers_dict[k.split('_')[0]] = {'value':v, 'option': True}  
    elif k.endswith('answer'):
        ques_answers_dict[k.split('_')[0]] = {'value':v, 'option': False} 
  
  edit_new_form = new_form.copy()
  for key in edit_new_form.keys():
    if key.endswith('answer'):
      new_form.pop(key)
  return render(request, 'nominate_app/nomination_instances/new.html', {'answers_form':answers_form,'nomination':nomination,'nomination_instance':nomination_instance, 'nomination_template':nomination_template, 'questions':questions })

def edit(request,nomination_id,nomination_instance_id):
  answers_form = NominationAnswersForm(instance=NominationAnswers())
  nomination = Nomination.objects.get(id=nomination_id)
  nomination_instance = NominationInstance.objects.get(id=nomination_instance_id)
  nomination_template = nomination.award_template
  questions = Questions.objects.filter(award_template = nomination_template,group=nomination.group).order_by('id')
  new_form = request.POST.copy()
  dict_new_form = dict(new_form)
  ques_answers_dict = {}
  for k, v in dict_new_form.items():
    if k.endswith('answer_option'):
      ques_answers_dict[k.split('_')[0]] = {'value':v, 'option': True}  
    elif k.endswith('answer'):
        ques_answers_dict[k.split('_')[0]] = {'value':v, 'option': False} 
  
  edit_new_form = new_form.copy()
  for key in edit_new_form.keys():
    if key.endswith('answer'):
      new_form.pop(key)
  return render(request, 'nominate_app/nomination_instances/new.html', {'answers_form':answers_form,'nomination':nomination,'nomination_instance':nomination_instance, 'nomination_template':nomination_template, 'questions':questions })

def nomination_instance(request,nomination_id,nomination_instance_id):
  answers_form = NominationAnswersForm(instance=NominationAnswers())
  nomination = Nomination.objects.get(id=nomination_id)
  nomination_instance = NominationInstance.objects.get(id=nomination_instance_id)
  nomination_template = nomination.award_template
  nom_answers = NominationAnswers.objects.filter(nomination_instance_id =nomination_instance,award_template_id=nomination_template).order_by('id')
  return render(request, 'nominate_app/nomination_instances/show.html', {'answers_form':answers_form,'nomination_chain':nomination_instance, 'nomination_template':nomination_template, 'nomination_answers': nom_answers })