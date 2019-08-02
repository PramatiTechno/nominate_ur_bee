from django.shortcuts import render
from nominate_app.models import Awards, AwardTemplate, NominationInstance, User, Nomination, Group
from django.http import HttpResponse
from django.core import serializers 
from django.http import JsonResponse
from IPython import embed
# Create your views here.

def home(request):
    return render(request, 'base.html')

def get_nomination_data(award):
  nomination_data = []
  
  award_templates = award.awardtemplate_set.all()
  frequency = award.frequency
  
  award_template_ids = [ award_template.id for award_template in award_templates ]
  nominations = Nomination.objects.filter(award_template_id__in=award_template_ids)
  for nomination in nominations:
    nd = {
      'start_day': nomination.start_day.strftime('%d %B'),
      'end_day': nomination.end_day.strftime('%d %B'),
      'group_name': nomination.group.name,
      'template_name':  nomination.award_template.template_name.capitalize(),
      'instances': []
    }
    for nomination_instance in nomination.nominationinstance_set.all():
      st = None
      for status in nomination_instance.statuses:
        if nomination_instance.status == status[1]:
          st = status[0]
      
      nd['instances'].append({
        'username': nomination_instance.user.username,
        'status': st,
      })
    
    nomination_data.append(nd)
  return nomination_data

def nomination_status(request):
  if request.method == 'GET':
    awards = Awards.objects.all()
    award = awards[0]
    nomination_data = get_nomination_data(award)
  return render(request, 'nominate_app/nomination_status.html',{'award_categories':awards, 'nominations': nomination_data, 'award_selected': award})
  #return render(request, 'nominate_app/nomination_status.html',{'nomination_status':nomination_status, 'award_categories':awards, 'nominations': nomination_data})

def nomination_status_load(request,id):
  
  if request.method == 'GET':
    awards = Awards.objects.all()
    award = Awards.objects.get(id=id)
    nomination_data = get_nomination_data(award)
    return render(request, 'nominate_app/nomination_status.html',{'award_categories':awards, 'nominations': nomination_data, 'award_selected': award})


