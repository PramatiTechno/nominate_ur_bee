from django.shortcuts import render
from nominate_app.models import Awards, AwardTemplate, NominationInstance, User
from django.http import HttpResponse
from django.core import serializers 
from django.http import JsonResponse
# Create your views here.

def home(request):
    return render(request, 'base.html')


def nomination_status(request):
  if request.method == 'GET':
    awards = Awards.objects.all()
    award_id = awards.first().id
    award_template_id = AwardTemplate.objects.get(award_id=award_id, is_active=True).id
    nomination_status = NominationInstance.objects.filter(award_template_id=award_template_id)
  return render(request, 'nominate_app/nomination_status.html',{'nomination_status':nomination_status, 'award_categories':awards})

def nomination_status_load(request,id):
	award = Awards.objects.get(id=request.GET["id"])
	data = []
	for user in User.objects.all():
	  record = {}
	  award_template = AwardTemplate.objects.get(award_id=award.id, is_active=True)
	  nominater = NominationInstance.objects.get(user_id=user.id)
	  record['nominator_name'] = user.__dict__['name']
	  record['nominator_status'] = nominater.__dict__['status']
	  data.append(record)
	return JsonResponse(data, safe=False)


