from django.shortcuts import render, redirect
from nominate_app.models import *
from nominate_app.forms import NominationStatusDateForm
from nominate_app.utils import group_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.core import serializers 
from datetime import datetime
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.db.models import Avg
from django.urls import reverse
import os
from IPython import embed
# Create your views here.

def home(request):
    return render(request, 'base.html')

def get_nomination_data(award_name, award_template_name, page, start_day=None, end_day=None):
  page = int(page)
  nomination_data = []

  award = None
  award_template = None
  award_exist = Awards.objects.filter(name=award_name).exists()
  award_template_exist = None

  if award_exist:
    award = Awards.objects.get(name=award_name)
    award_template_exist = AwardTemplate.objects.filter(award=award, template_name=award_template_name).exists()
    if award_template_exist:
      award_template = AwardTemplate.objects.get(award=award, template_name=award_template_name)
      nominations = Nomination.objects.filter(award_template_id=award_template.id).order_by('id')

  submissions = NominationSubmitted.objects.filter(award_name=award_name, template_name=award_template_name)
  if submissions:
    submitted_nominations = Nomination.objects.filter(id__in=submissions.values('nomination_id'))

  if start_day and end_day:
    if start_day < end_day:
      if award_template_exist:
        nominations = nominations.filter(nomination_timing__start_day__gte=start_day, nomination_timing__approval_end_day__lte=end_day)
      if submissions:
        submitted_nominations = submitted_nominations.filter(nomination_timing__start_day__gte=start_day, nomination_timing__approval_end_day__lte=end_day)


  if award_template_exist:
    if submissions:
      nominations = nominations.union(submitted_nominations)
  else:
    nominations = submitted_nominations


  paginator = Paginator(nominations, 9)
  try:
    nominations = paginator.page(page)
  except PageNotAnInteger:
    nominations = paginator.page(1)
  except EmptyPage:
    nominations = paginator.page(paginator.num_pages)

  for nomination in nominations:
    nd = {
      'start_day': nomination.start_day.strftime('%d %B'),
      'end_day': nomination.end_day.strftime('%d %B'),
      'end_day_data': nomination.end_day,
      'group_name': nomination.group.name,
      'template_name':  nomination.award_template.template_name.capitalize() if nomination.award_template else 'unknown template',
      'nomination_id': nomination.id,
      'instances': []
    }
    if nomination.group.name == 'Technical Jury Member':
      nd['review_start_day'] = nomination.review_start_day.strftime('%d %B')
      nd['review_end_day'] = nomination.review_end_day.strftime('%d %B')
      nd['review_end_day_data'] = nomination.review_end_day

    if nomination.group.name == 'Directorial Board Member':
      nd['approval_start_day'] = nomination.approval_start_day.strftime('%d %B')
      nd['approval_end_day'] = nomination.approval_end_day.strftime('%d %B')
      nd['approval_end_day_data'] = nomination.approval_end_day

    users = User.objects.filter(groups__id=nomination.group_id)
    for user in users:
      nomination_submitted = NominationSubmitted.objects.filter(template_name=award_template_name, email=user.email)
      nomination_instance = None
      if award_template_exist:
        nomination_instance = NominationInstance.objects.filter(nomination__award_template_id=nomination.award_template_id, user=user)

      nomination_rating = NominationRating.objects.all()
      if nomination_submitted:
        nd['instances'].append({
            'username': user.email,
            'status': nomination_submitted[0].get_status(nomination_submitted[0].status),
            'id': nomination_submitted[0].id,
            'avg_rating': nomination_rating.filter(submission_id=nomination_submitted[0].id).\
              aggregate(Avg('rating'))['rating__avg'] if nomination_submitted[0].ratings.all() else 0.0,
            'is_active': bool(nomination_instance)
        })  
      elif nomination_instance:
          nd['instances'].append({
              'username': user.email,
              'status': nomination_instance[0].get_status(nomination_instance[0].status),
              'id': None,
              'avg_rating': 0.0,
              'is_active': True
          })
      else:
          nd['instances'].append({
              'username': user.email,
              'status': "New",
              'id': None,
              'avg_rating': 0.0,
              'is_active': True
          })
      nomination_data.append(nd)
  nominations.object_list = nomination_data
  return nominations



def get_nomination_details(page, award_name=None, template_name=None, start_day=None, end_day=None):  
  date_form = NominationStatusDateForm()
  submitted_awards =  NominationSubmitted.objects.all().values_list('award_name', flat=True).distinct() 
  awards = Awards.objects.all().values_list('name', flat=True).distinct()
  union_awards = submitted_awards.union(awards)

  award_exist = Awards.objects.filter(name=award_name).exists()
  submissions = NominationSubmitted.objects.filter(award_name=award_name)

  if award_exist:
    award = Awards.objects.get(name=award_name)
    award_templates = [template.template_name for template in award.awardtemplate_set.all()]
    if award_exist and submissions:
      submission_templates = list(submissions.values_list('template_name', flat=True).distinct())
      award_templates = list(set(award_templates + submission_templates))
  elif submissions:
    award_templates = submissions.values_list('template_name', flat=True).distinct()

  nomination_data = None
  if start_day and end_day:
    date_form.initial['from_'] = start_day
    date_form.initial['to'] = end_day
    start_day = datetime.strptime(start_day, '%m/%d/%Y').date()
    end_day = datetime.strptime(end_day, '%m/%d/%Y').date()

  if award_templates:
    if template_name:
      award_template = template_name
    else:
      award_template = award_templates[0]
    nomination_data = get_nomination_data(award_name, award_template, page, start_day=start_day, end_day=end_day)
  else:
    award_template = None

  return {
    'award_categories': union_awards, 
    'nominations': nomination_data, 
    'award_selected': award_name, 
    'award_templates': award_templates, 
    'selected_template': award_template,
    'date_form': date_form
  }


@group_required('Admin', raise_exception=True)
def nomination_status(request):
  if request.method == 'GET':
    page = request.GET.get('page', 1)

    if 'award_name' in request.GET:
      award_name = request.GET['award_name']
      if 'template_name' in request.GET:
        template_name = request.GET['template_name']
        if 'from_' and 'to' in request.GET:
          start_day = request.GET['from_']
          end_day = request.GET['to']
          if start_day > end_day:
            messages.error(request, "End date must be greater than start date.")
          return render(request, 'nominate_app/nomination_status.html', get_nomination_details(page, award_name=award_name, template_name=template_name, start_day=start_day, end_day=end_day))
        return render(request, 'nominate_app/nomination_status.html', get_nomination_details(page, award_name=award_name, template_name=template_name))
      return render(request, 'nominate_app/nomination_status.html', get_nomination_details(page, award_name=award_name))

    submitted_awards =  NominationSubmitted.objects.all().values_list('award_name', flat=True).distinct() 
    awards = Awards.objects.all().values_list('name', flat=True).distinct()
    union_awards = submitted_awards.union(awards)
    if union_awards:
      award = union_awards[0]
      return render(request, 'nominate_app/nomination_status.html', get_nomination_details(page, award_name=award))
    else: 
      return render(request, 'nominate_app/nomination_status.html')


@group_required('Admin', raise_exception=True)
def email(request, username, nomination_id):
  users = User.objects.filter(email=username)
  nomination = Nomination.objects.get(id=nomination_id)
  award_template = nomination.award_template.template_name
  end_day = nomination.end_day
  award_name = nomination.award_template.award.name
  template_name = 'nominate_app/emails/reminder.html'
  instance=nomination.nominationinstance_set.filter(user__email=users.first())
  subjects = { 
              0:['Reminder to Review the Nominations', 'review'], 
              1:['Reminder to Approve the Nominations', 'approve/decline'],
              4:['Reminder to Approve the Nominations', 'approve/decline']
              }  
  try:
    if not instance:
      new_status = "submit"
      subject = 'Reminder to Submit your Nominations'
      link = str(os.environ['SERVER_NAME'] + reverse('nominate_app:nominations'))
    elif instance and instance.first().get_status(instance.first().status)=='Saved':
      new_status = "submit"
      subject = 'Reminder to Submit your Nominations'
      link = str(os.environ['SERVER_NAME'] + reverse('nominate_app:nominations'))
    else:
      submission = nomination.submissions.get(email=users.first().email)
      if submission.status == 0:
        users = User.objects.filter(groups__name='Technical Jury Member')
        end_day = nomination.review_end_day
        link = str(os.environ['SERVER_NAME'] + reverse('nominate_app:nomination_review_index'))
      elif submission.status in [1, 4]:
        users  = User.objects.filter(groups__name='Directorial Board Member')
        end_day = nomination.approval_end_day
        link = str(os.environ['SERVER_NAME'] + reverse('nominate_app:approval'))
      new_status = subjects[submission.status][1]
      subject = subjects[submission.status][0]
    for user in users:
      message_value_html_template = render_to_string(template_name,\
      {'name':user.userprofile.get_username(), 'award_template':award_template, \
        'award_name':award_name, 'end_day':end_day, 'new_status':new_status, \
          'link':link })
      plain_message_value = strip_tags(message_value_html_template)
      send_mail(subject=subject, html_message=message_value_html_template, from_email='no-reply@pramati.com', \
      recipient_list=[str(user.email)], message=plain_message_value, fail_silently=False)
  except Exception as e: 
    return JsonResponse({'status':'unsent'})
  return JsonResponse({'status':'sent'})