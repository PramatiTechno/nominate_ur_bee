from django.shortcuts import render
from nominate_app.models import Awards, AwardTemplate, NominationInstance, User
from django.http import HttpResponse
from django.core import serializers 
from django.http import JsonResponse
from IPython import embed
# Create your views here.

def home(request):
    return render(request, 'base.html')


def nomination_status(request):
  if request.method == 'GET':
    awards = Awards.objects.all()
    if awards.count()==0:
      nomination_status = []
    else:
      award_id = awards.first().id
      award_template_id = AwardTemplate.objects.filter(award_id=award_id).values_list('id', flat=True)
      try:
        nomination_status = NominationInstance.objects.filter(pk__in=[award_template_id])
      except:
        nomination_status = []
  return render(request, 'nominate_app/nomination_status.html',{'nomination_status':nomination_status, 'award_categories':awards})

def nomination_status_load(request,id):
  award = Awards.objects.get(id=id)
  data = []
  role = Role.objects.filter(name='Manager').first()
  user_roles = UserRole.objects.filter(role=role)
  for user_role in user_roles:
    record = {}
    user = user_role.user
    award_template = AwardTemplate.objects.get(award_id=award, is_active=True)
    nominater = NominationInstance.objects.get(user_id=user, award_template_id=award_template)
    record['nominator_name'] = user.username
    record['nominator_status'] = nominater.status
    data.append(record)
  return JsonResponse(data, safe=False)


