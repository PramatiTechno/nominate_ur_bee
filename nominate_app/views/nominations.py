from django.shortcuts import render, redirect
from nominate_app.models import NominationPeriod, Awards
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponse
from nominate_app.forms import AwardsForm, AwardsActiveForm, NominationPeriodForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from nominate_app.utils import group_required
from nominate_app.models import Nomination,NominationPeriod, AwardTemplate, NominationInstance, User, Questions, NominationAnswers
from IPython import embed
from datetime import datetime

def change_date(request, nomination_id):
  nomination = Nomination.objects.get(id=nomination_id)
  date = request.POST['date']
  nomination.end_day = datetime.strptime(date, '%m/%d/%Y').date()
  nomination.save()
  return redirect('nominate_app:nomination_status') 

def index(request):
  current_user = User.objects.get(id=request.user.id)
  nominations = Nomination.objects.filter(group__in=list(map(lambda x: x['id'],current_user.groups.values()))) #,start_day__gt= datetime.today(),end_day__lt= datetime.today() )#list(map(lambda g: g.id,current_user.groups.all()))) 
  new_nominations,saved_nominations,submitted_nominations = [],[],[]
  for nomination in nominations:
      nomination_instance = nomination.nominationinstance_set.filter(user=request.user)
      if nomination_instance.count() == 0:
        new_nominations.append(nomination)        
      elif nomination_instance[0].status == 1:
        nomination.nomination_instance_id = nomination_instance[0].id
        saved_nominations.append(nomination)
      elif nomination_instance[0].status == 2:
        nomination.nomination_instance_id = nomination_instance[0].id
        submitted_nominations.append(nomination)    
  return render(request, 'nominate_app/nominations/index.html', {'new_nominations': new_nominations, 'submitted_nominations':submitted_nominations, 'saved_nominations': saved_nominations })

