from django.shortcuts import render, redirect 
from nominate_app.utils import group_required
from django.forms import modelformset_factory, inlineformset_factory
from nominate_app.forms import NominationAnswersForm
from nominate_app.models import Nomination,NominationPeriod, AwardTemplate, NominationInstance, User, Questions, NominationAnswers, NominationSubmitted, QuestionAnswers, UserProfile
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.template.defaulttags import register
from django.core.files.storage import FileSystemStorage
import json
from django.utils import timezone
import os
from django.conf import settings
from datetime import datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from IPython import embed

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@group_required('Directorial Board Member', 'Technical Jury Member', 'Manager', raise_exception=True)
def index(request,nomination_id):
  if request.method == 'POST':  
    answers_form = NominationAnswersForm(instance=NominationAnswers())
    nomination = Nomination.objects.get(id=nomination_id)
    nomination_instance = NominationInstance.objects.get_or_create(nomination=nomination,user=request.user)[0]
    nomination_template = nomination.award_template
    questions = Questions.objects.filter(award_template = nomination_template,groups=nomination.group).order_by('id')
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

      nomination_answers = NominationAnswers.objects.filter(nomination_instance_id=nomination_instance.id)
      for ans in ans_obj_List:
        try:
          condition1 = Q(nomination_instance_id=nomination_instance.id)
          condition2 = Q(question_id=ans['question'])
          file = request.FILES.getlist(ans['question']+'_attachment_path')
          ans['file_url'] = None
          if file:
            file = file[0]
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            ans['file_url'] = fs.url(filename)

          na = NominationAnswers.objects.get(condition1 & condition2)
          if ans['option']:
            na.answer_text = json.dumps(ans['answer_text'])
          else:
            na.answer_text = ans['answer_text'][0]

          na.answer_option = ans['option']
          if ans['file_url']:
            na.attachment_path = ans['file_url']
          else:
            ans['file_url'] = na.attachment_path

          na.save()

        except Exception as e:
          print(e)
          if ans['option']:
            answer_text = json.dumps(ans['answer_text'])
          else:
            answer_text = ans['answer_text'][0]

          file = request.FILES.getlist(ans['question']+'_attachment_path')
          ans['file_url'] = None
          if file:
            file = file[0]
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            ans['file_url'] = fs.url(filename)

          na = NominationAnswers(answer_option=ans['option'], answer_text=answer_text, attachment_path=ans['file_url'], nomination_instance_id=nomination_instance.id, uploaded_at=timezone.now(), award_template_id=ans['award_template'],question_id=ans['question'], submitted_by=request.user)
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
              question=Questions.objects.get(id=ans_obj['question']).qname, answer=answer_text, attachment_path=ans_obj['file_url'])
            qa.save()
        nomination_instance.status = 2
        nomination_instance.submitted_at = timezone.now()
        nomination_instance.save()
        to_tech_jury = User.objects.filter(groups__name='Technical Jury Member')
        subject_manager = "Nominations Submitted !!!"
        subject_tech_jury = "Nominations submitted by " + str(request.user.first_name) +\
           " " + str(request.user.last_name)
        message_value_html_template = render_to_string('nominate_app/emails/congratulate_manager.html', \
          {'manager_name':request.user.first_name, 'template':nomination_instance.nomination.award_template})
        plain_message_value = strip_tags(message_value_html_template)
        send_mail(subject=subject_manager, from_email='no-reply@pramati.com', \
          recipient_list=[str(request.user.email)], \
            message=plain_message_value, fail_silently=False)
        for jury in to_tech_jury:
          message_value_html_template = render_to_string('nominate_app/emails/tech_jury_notify_submission.html', \
            {'manager_name':request.user.first_name, 'tech_jury_name':jury.username, \
              'template':nomination_instance.nomination.award_template})
          plain_message_value = strip_tags(message_value_html_template)          
          send_mail(subject=subject_tech_jury, from_email='no-reply@pramati.com', \
            recipient_list=[str(jury.email)], message=plain_message_value, fail_silently=False)
        messages.success(request, 'Nomination submitted successfully.')
      return redirect('nominate_app:nominations')


@group_required('Directorial Board Member', 'Technical Jury Member', 'Manager', raise_exception=True)
def new(request,nomination_id):
  answers_form = NominationAnswersForm(instance=NominationAnswers())
  nomination = Nomination.objects.get(id=nomination_id)
  nomination_instance = NominationInstance(nomination=nomination)
  
  nomination_template = nomination.award_template
  questions = Questions.objects.filter(award_template = nomination_template,groups=nomination.group).order_by('id')
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


@group_required('Directorial Board Member', 'Technical Jury Member', 'Manager', raise_exception=True)
def edit(request,nomination_id,nomination_instance_id):
  answers_form = NominationAnswersForm(instance=NominationAnswers())
  nomination = Nomination.objects.get(id=nomination_id)
  nomination_instance = NominationInstance.objects.get(id=nomination_instance_id)
  nomination_template = nomination.award_template
  questions = Questions.objects.filter(award_template = nomination_template,groups=nomination.group).order_by('id')
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
  qanswers = []
  for question in questions:
    try:
      answer = question.nominationanswers_set.get(submitted_by=request.user.id)
      answer_text = answer.answer_text
      attachment_path = str(answer.attachment_path)
      if question.qtype == "SUBJECTIVE":
        qanswers.append({
          'question': question,
          'answer_text': answer_text,
          'attachment_path': attachment_path
        })
      else:
         qanswers.append({
          'question': question,
          'answer_text': json.loads(answer_text),
          'attachment_path': attachment_path
        })
    except:
      qanswers.append({
        'question': question
      })
      

  return render(request, 'nominate_app/nomination_instances/edit.html', {'answers_form':answers_form,'nomination':nomination,'nomination_instance':nomination_instance, 'nomination_template':nomination_template, 'qanswers': qanswers })


@group_required('Directorial Board Member', 'Technical Jury Member', 'Manager', raise_exception=True)
def submitted_nomination(request, nomination_submitted_id):
  qa = QuestionAnswers.objects.filter(nomination_submitted_id=nomination_submitted_id)
  qa_set = []
  for question in qa:
    qa_set.append({
      'qa': question,
      'attachment_path': str(question.attachment_path)
    })
  return render(request, 'nominate_app/nomination_instances/show.html', {'question_answerset':qa_set, 'nomination_submitted':NominationSubmitted.objects.get(id=nomination_submitted_id)})


@group_required('Directorial Board Member', 'Technical Jury Member', 'Manager', raise_exception=True)
def nomination_instance(request,nomination_id,nomination_instance_id):
  answers_form = NominationAnswersForm(instance=NominationAnswers())
  nomination = Nomination.objects.get(id=nomination_id)
  nomination_instance = NominationInstance.objects.get(id=nomination_instance_id)
  nomination_template = nomination.award_template
  nom_answers = NominationAnswers.objects.filter(nomination_instance_id =nomination_instance,award_template_id=nomination_template).order_by('id')
  return render(request, 'nominate_app/nomination_instances/show.html', {'answers_form':answers_form,'nomination_chain':nomination_instance, 'nomination_template':nomination_template, 'nomination_answers': nom_answers })
