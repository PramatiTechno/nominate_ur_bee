from django.shortcuts import render, redirect 
from django.forms import modelformset_factory, inlineformset_factory
from nominate_app.forms import NominationAnswersForm
from nominate_app.models import Nomination,NominationPeriod, AwardTemplate, NominationInstance, User, Questions, NominationAnswers, NominationSubmitted, QuestionAnswers, UserProfile
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.template.defaulttags import register
import json
from django.utils import timezone
import os
from django.conf import settings
from datetime import datetime
from IPython import embed

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

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
          if ans['option']:
            na.answer_text = json.dumps(ans['answer_text'])
          else:
            na.answer_text = ans['answer_text'][0]
          na.answer_option = ans['option']
          na.save()
        except Exception as e:
          print(e)
          if ans['option']:
            answer_text = json.dumps(ans['answer_text'])
          else:
            answer_text = ans['answer_text'][0]

          na = NominationAnswers(answer_option=ans['option'], answer_text=answer_text,nomination_instance_id=nomination_instance.id, uploaded_at=timezone.now(), award_template_id=ans['award_template'],question_id=ans['question'], submitted_by=request.user)
          na.save()

      # This code to be refactored. Multiple answer records submit
      if request.POST['action'] == 'save':
        nomination_instance.status = 1
        nomination_instance.save()
        messages.success(request, 'Nomination saved successfully.')
      elif request.POST['action'] == 'submit':
        user_details = UserProfile.objects.get(user_id=request.user.id)
        nomination_submitted = NominationSubmitted(status=0, email=request.user.username, firstname=request.user.first_name, \
          lastname=request.user.last_name, nomination_id=nomination.id, award_name=nomination_template.award.name, \
          group_id=request.user.groups.all()[0].id, designation=user_details.designation, \
          worklocation=user_details.worklocation, baselocation=user_details.baselocation, \
          template_name=nomination_template.template_name, submitted_at=timezone.now())
        nomination_submitted.save()
        for ans_obj in ans_obj_List:
          if ans_obj['action'] == 'submit':
            answer_text = ", ".join(ans_obj['answer_text'])
            qa = QuestionAnswers(nomination_submitted_id=nomination_submitted.id, \
              question=Questions.objects.get(id=ans_obj['question']).qname, answer=answer_text)
            qa.save()
        nomination_instance.status = 2
        nomination_instance.submitted_at = timezone.now()
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
  answers = {}
  for question in questions:
    try:
      answer_text = question.nominationanswers_set.get(submitted_by=request.user.id).answer_text
      if question.qtype == "SUBJECTIVE":
        answers[question.id] = answer_text
      else:
        answers[question.id] = json.loads(answer_text)
    except:
      answers[question.id] = []
      

  return render(request, 'nominate_app/nomination_instances/edit.html', {'answers_form':answers_form,'nomination':nomination,'nomination_instance':nomination_instance, 'nomination_template':nomination_template, 'questions':questions, 'answers': answers })

def submitted_nomination(request, nomination_submitted_id):
  qa = QuestionAnswers.objects.filter(nomination_submitted_id=nomination_submitted_id)
  return render(request, 'nominate_app/nomination_instances/show.html', {'question_answerset':qa, 'nomination_submitted':NominationSubmitted.objects.get(id=nomination_submitted_id)})

def nomination_instance(request,nomination_id,nomination_instance_id):
  answers_form = NominationAnswersForm(instance=NominationAnswers())
  nomination = Nomination.objects.get(id=nomination_id)
  nomination_instance = NominationInstance.objects.get(id=nomination_instance_id)
  nomination_template = nomination.award_template
  nom_answers = NominationAnswers.objects.filter(nomination_instance_id =nomination_instance,award_template_id=nomination_template).order_by('id')
  return render(request, 'nominate_app/nomination_instances/show.html', {'answers_form':answers_form,'nomination_chain':nomination_instance, 'nomination_template':nomination_template, 'nomination_answers': nom_answers })
