from django.shortcuts import render, redirect
from nominate_app.models import NominationPeriod, Awards
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponse
from nominate_app.forms import AwardsForm, AwardsActiveForm, NominationPeriodForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.template.defaulttags import register
from nominate_app.utils import group_required
from nominate_app.models import Nomination,NominationPeriod, AwardTemplate, NominationInstance, User, Questions, NominationAnswers, NominationSubmitted
from IPython import embed
from datetime import datetime

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def change_date(request, nomination_id):
  nomination = Nomination.objects.get(id=nomination_id)
  date = request.POST['date']
  nomination.end_day = datetime.strptime(date, '%m/%d/%Y').date()
  nomination.save()
  return redirect('nominate_app:nomination_status') 

def index(request):
  
  current_user = User.objects.get(id=request.user.id)
  nominations = Nomination.objects.filter(group__in=list(map(lambda x: x['id'],current_user.groups.values()))) #,start_day__gt= datetime.today(),end_day__lt= datetime.today() )#list(map(lambda g: g.id,current_user.groups.all()))) 
  new_nominations = []
  
  for nomination in nominations:
      nomination_instance = nomination.nominationinstance_set.filter(user=request.user)
      if nomination_instance.count() == 0:
        new_nominations.append(nomination)   
  statuses = ['New', 'Saved']
  statuses.extend(status[0] for status in NominationSubmitted.statuses)
  page = request.GET.get('page', 1)
  paginator = Paginator(new_nominations, 9)
  try:
    nominations = paginator.page(page)
  except PageNotAnInteger:
    nominations = paginator.page(1)
  except EmptyPage:
    nominations = paginator.page(paginator.num_pages)
  return render(request, 'nominate_app/nominations/index.html', {'data': nominations, 'statuses': statuses, 'selected_status': "new" })

def status_index(request, status_value):
  current_user = User.objects.get(id=request.user.id)
  statuses = ['New', 'Saved']
  nomination_data = []
  statuses.extend(status[0] for status in NominationSubmitted.statuses)
  
  if status_value.lower() == "new":
    
    return redirect('nominate_app:nominations')
  elif status_value.lower() == "saved":
    nominations = Nomination.objects.filter(group__in=list(map(lambda x: x['id'],current_user.groups.values())))
    for nomination in nominations:
      nomination_instance = nomination.nominationinstance_set.filter(user=request.user)
      if nomination_instance and nomination_instance[0].status == 1:
        nomination.nomination_instance_id = nomination_instance[0].id
        nomination_data.append(nomination)
  elif status_value.lower() == "submitted":
    nomination_data = NominationSubmitted.objects.filter(status=0)
  elif status_value.lower() == "reviewed":
    nomination_data = NominationSubmitted.objects.filter(status=1)
  elif status_value.lower() == "approved":
    nomination_data = NominationSubmitted.objects.filter(status=2)
  elif status_value.lower() == "dismissed":
    nomination_data = NominationSubmitted.objects.filter(status=3)
  else:
    nomination_data = NominationSubmitted.objects.filter(status=4)
  page = request.GET.get('page', 1)
  paginator = Paginator(nomination_data, 9)
  try:
    nominations = paginator.page(page)
  except PageNotAnInteger:
    nominations = paginator.page(1)
  except EmptyPage:
    nominations = paginator.page(paginator.num_pages)
  
  return render(request, 'nominate_app/nominations/index.html', {'data': nominations, 'statuses': statuses, 'selected_status': status_value.lower() })