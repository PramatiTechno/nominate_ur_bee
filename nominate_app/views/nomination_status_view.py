from django.shortcuts import render, redirect
from nominate_app.models import Awards, AwardTemplate, NominationInstance, User, Nomination, Group, NominationSubmitted, NominationRating
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.core import serializers 
from django.http import JsonResponse
from IPython import embed
from datetime import datetime
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.db.models import Avg

# Create your views here.

def home(request):
    return render(request, 'base.html')

def get_nomination_data(award_ft_submissions, award_name, award_template_name, page, start_day=None, end_day=None, request=None):
  page = int(page)
  nomination_data = []
  award = Awards.objects.get(name=award_name)
  award_template = AwardTemplate.objects.get(award=award, template_name=award_template_name)

  if start_day and end_day and start_day < end_day:
    nominations = Nomination.objects.filter(award_template=award_template, start_day__gte=start_day, end_day__lte=end_day)
  else:
    if start_day and end_day:
      messages.error(request, "End date must be greater than start date.")

    nominations = Nomination.objects.filter(award_template_id=award_template.id).order_by('id')

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
      'template_name':  nomination.award_template.template_name.capitalize(),
      'nomination_id': nomination.id,
      'instances': []
    }
    users = User.objects.filter(groups__id=nomination.group_id)
    for user in users:
      nomination_submitted = NominationSubmitted.objects.filter(template_name=nomination.award_template.template_name, email=user.email)
      nomination_instance = NominationInstance.objects.filter(nomination__award_template_id=nomination.award_template_id, user=user)
      nomination_rating = NominationRating.objects.all()
      if nomination_submitted:
        if nomination_instance:
          nd['instances'].append({
              'username': user.email,
              'status': nomination_submitted[0].get_status(nomination_submitted[0].status),
              'id': nomination_instance[0].id,
              'avg_rating': nomination_rating.filter(submission_id=nomination_submitted[0].id).\
                aggregate(Avg('rating'))['rating__avg'] if nomination_submitted[0].ratings.all() else 0.0
          })
        else:
          nd['instances'].append({
              'username': user.email,
              'status': nomination_submitted[0].get_status(nomination_submitted[0].status),
              'id': None,
              'rating':nomination_rating.filter(submission_id=nomination_submitted[0].id).\
                aggregate(Avg('rating'))['rating__avg'] if nomination_submitted[0].ratings.all() else 0.0
          })          

      elif nomination_instance:
          nd['instances'].append({
              'username': user.email,
              'status': nomination_instance[0].get_status(nomination_instance[0].status),
              'id': nomination_instance[0].id,
              'rating': None
          })
      else:
          nd['instances'].append({
              'username': user.email,
              'status': "New",
              'id': None,
              'rating': None
          })
      nomination_data.append(nd)
  nominations.object_list = nomination_data
  return nominations


def nomination_status(request):
  if request.method == 'GET':
    awards =  NominationSubmitted.objects.all().values_list('award_name', flat=True).distinct() 
    sub = Awards.objects.all().values_list('name', flat=True).distinct()
    page = request.GET.get('page', 1)
    if awards:
      intersection = awards.intersection(sub)
      award = intersection[0]
      return render(request, 'nominate_app/nomination_status.html', get_nomination_details(page, award_name=award))
    else: 
      return render(request, 'nominate_app/nomination_status.html')

def nomination_status_load(request, award_name):
  if request.method == 'GET':
    # award = Awards.objects.get(id=id)
    page = request.GET.get('page', 1)
    return render(request, 'nominate_app/nomination_status.html', get_nomination_details(page, award_name=award_name))

def nomination_status_load_filter(request, award_name, template_name):
  page = request.GET.get('page', 1)
  days = request.GET.getlist('filter')
  start_day = datetime.strptime(days[0], '%m/%d/%Y').date()
  end_day = datetime.strptime(days[1], '%m/%d/%Y').date()
  return render(request, 'nominate_app/nomination_status.html', get_nomination_details(page, award_name=award_name, template_name=template_name, start_day=start_day, end_day=end_day, request=request))


def get_nomination_details(page, award_name=None, template_name=None, start_day=None, end_day=None, request=None):
  submissions = NominationSubmitted.objects.all()
  awards = submissions.values_list('award_name', flat=True).distinct()
  if award_name:
    award = award_name
  else:
    award = awards[0]

  award_ft_submissions = submissions.filter(award_name=award)
  ats =[ award_template.template_name for award_template in  AwardTemplate.objects.all()]

  award_templates = award_ft_submissions.values_list('template_name', flat=True).distinct()
  ats.extend(award_templates)
  award_templates = list(set(ats))
  award_templates.sort()
  nomination_data = None

  if award_templates:
    if template_name:
      award_template = template_name
    else:
      award_template = award_templates[0]
    nomination_data = get_nomination_data(award_ft_submissions, award, award_template, page, start_day=start_day, end_day=end_day, request=request)
  else:
    award_template = None

  return {'award_categories': awards, 'nominations': nomination_data, 'award_selected': award, 'award_templates': award_templates, 'selected_template': award_template}


def nomination_status_load_template(request, award_name, template_name):
  if request.method == 'GET':
    page = request.GET.get('page', 1)
    return render(request, 'nominate_app/nomination_status.html', get_nomination_details(page, award_name=award_name, template_name=template_name))

def email(request, nomination, nomination_id):
  subject = "Reminder mail"
  user = User.objects.get(username=nomination)
  nomination = Nomination.objects.get(id=nomination_id)
  award_template = nomination.award_template.template_name
  end_day = nomination.end_day
  award_name = nomination.award_template.award.name
  template_name = 'nominate_app/emails/reminder.html'
  new_status_dict = {0:'nominate',2:'review',3:'approve/decline',6:'approve/decline'}
  new_status = new_status_dict[nomination.nominationinstance_set.all()[0].status]
  message_value_html_template = render_to_string(template_name,\
  {'name':user.username, 'award_template':award_template, \
    'award_name':award_name, 'end_day':end_day, 'new_status':new_status})
  plain_message_value = strip_tags(message_value_html_template)
  send_mail(subject=subject, from_email='no-reply@pramati.com', \
    recipient_list=[str(user.email)], message=plain_message_value, fail_silently=False)
  return redirect('nominate_app:nomination_status')