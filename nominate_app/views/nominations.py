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


def index(request):
  current_user = User.objects.get(id=request.user.id)
  nominations = Nomination.objects.filter(group__in=list(map(lambda x: x['id'],current_user.groups.values()))) #,start_day__gt= datetime.today(),end_day__lt= datetime.today() )#list(map(lambda g: g.id,current_user.groups.all()))) 
  new_nominations,saved_nominations,submitted_nominations = [],[],[]
  for nomination in nominations:
      if nomination.nominationinstance_set.count() == 0:
        new_nominations.append(nomination)                                   
      elif nomination.nominationinstance_set.get(user=request.user).status == 1:
        nomination.nomination_instance_id = nomination.nominationinstance_set.get(user=request.user).id
        saved_nominations.append(nomination)
      elif nomination.nominationinstance_set.get(user=request.user).status == 2:
        nomination.nomination_instance_id = nomination.nominationinstance_set.get(user=request.user).id
        submitted_nominations.append(nomination)    
  return render(request, 'nominate_app/nominations/index.html', {'new_nominations': new_nominations, 'submitted_nominations':submitted_nominations, 'saved_nominations': saved_nominations })

