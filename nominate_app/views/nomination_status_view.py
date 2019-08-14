from django.shortcuts import render
from nominate_app.models import Awards, AwardTemplate, NominationInstance, User, Nomination, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.core import serializers 
from django.http import JsonResponse
from IPython import embed
from datetime import datetime
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'base.html')

def get_nomination_data(award_template, page, start_day=None, end_day=None, request=None):
  page = int(page)
  nomination_data = []
  nominations = None
  if start_day and end_day and start_day < end_day:
    nominations = Nomination.objects.filter(award_template_id=award_template.id, start_day__gte=start_day, end_day__lte=end_day)
  else:
    if start_day and end_day:
      messages.error(request, "End date must be greater than start date.")

    nominations = Nomination.objects.filter(award_template_id=award_template.id).order_by('id')
  paginator = Paginator(nominations, 9)
  try:
    numbers = paginator.page(page)
  except PageNotAnInteger:
    numbers = paginator.page(1)
  except EmptyPage:
    numbers = paginator.page(paginator.num_pages)
  for nomination in numbers:
    nd = {
      'start_day': nomination.start_day.strftime('%d %B'),
      'end_day': nomination.end_day.strftime('%d %B'),
      'end_day_data': nomination.end_day,
      'group_name': nomination.group.name,
      'template_name':  nomination.award_template.template_name.capitalize(),
      'nomination_id': nomination.id,
      'instances': []
    }
    for nomination_instance in nomination.nominationinstance_set.all().order_by('id'):
      st = None
      for status in nomination_instance.statuses:
        if nomination_instance.status == status[1]:
          st = status[0]
      
      nd['instances'].append({
        'username': nomination_instance.user.username,
        'status': st,
        'id': nomination_instance.id,
      })
    
    nomination_data.append(nd)
  numbers.object_list = nomination_data
  return numbers

def nomination_status(request):
  if request.method == 'GET':
    award = Awards.objects.first()
    page = request.GET.get('page', 1)
    if award:
      return render(request, 'nominate_app/nomination_status.html', get_nomination_details(page, id=award.id))
    else: 
      return render(request, 'nominate_app/nomination_status.html')

      

def nomination_status_load(request,id):
  if request.method == 'GET':
    award = Awards.objects.get(id=id)
    page = request.GET.get('page', 1)
    return render(request, 'nominate_app/nomination_status.html', get_nomination_details(page, id=award.id))

def nomination_status_load_filter(request,id, template_id):
  page = request.GET.get('page', 1)
  days = request.GET.getlist('filter')
  start_day = datetime.strptime(days[0], '%m/%d/%Y').date()
  end_day = datetime.strptime(days[1], '%m/%d/%Y').date()
  return render(request, 'nominate_app/nomination_status.html', get_nomination_details(page, id=id,template_id=template_id, start_day=start_day, end_day=end_day, request=request))


def get_nomination_details(page, id=None, template_id=None, start_day=None, end_day=None, request=None):
  awards = Awards.objects.all().order_by('id')
  if id:
    award = Awards.objects.get(id=id)
  else:
    award = awards[0]
  award_templates =  AwardTemplate.objects.filter(award_id=award.id).order_by('id')
  nomination_data = None
  if award_templates:
    if template_id:
      award_template = AwardTemplate.objects.get(id=template_id)
    else:
      award_template = AwardTemplate.objects.first()
    nomination_data = get_nomination_data(award_template, page, start_day=start_day, end_day=end_day, request=request)
  else:
    award_template = None
  return {'award_categories':awards, 'nominations': nomination_data, 'award_selected': award, 'award_templates': award_templates, 'selected_template': award_template}

def nomination_status_load_template(request, id, template_id):
  if request.method == 'GET':
    page = request.GET.get('page', 1)
    return render(request, 'nominate_app/nomination_status.html', get_nomination_details(page, id=id, template_id=template_id))
