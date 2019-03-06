from django.shortcuts import render
from nominate_app.models import Awards, AwardTemplate, NominationInstance
from django.http import HttpResponse
from django.core import serializers 

# Create your views here.

def home(request):
    return render(request, 'base.html')


def nomination_status(request):
    if request.method == 'GET':
        award_forms = Awards.objects.all()
        award_id = award_forms.first().id
        award_template_id = AwardTemplate.objects.get(award_id=award_id, is_active=True).id
        nomination_status = NominationInstance.objects.filter(award_template_id=award_template_id)
        # import IPython;IPython.embed()
    return render(request, 'nominate_app/nomination_status.html',{'nomination_status':nomination_status, 'award_forms':award_forms})

def nomination_status_load(request,id):
	award_forms = Awards.objects.all()
	award_template_id = AwardTemplate.objects.get(award_id=id, is_active=True).id
	load_templates = NominationInstance.objects.filter(award_template_id=award_template_id)
	to_json = serializers.serialize('json', load_templates)
	return HttpResponse(to_json, content_type='application/json')