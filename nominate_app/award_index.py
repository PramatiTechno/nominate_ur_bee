from django.shortcuts import render
from nominate_app.models import Awards, AwardTemplate
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse 

# Create your views here.

def home(request):
    return render(request, 'base.html')


def view_awards(request):
    if request.method == 'GET':
        forms = Awards.objects.all()
    return render(request, 'view_awards.html',{'forms':forms})


def edit_awards(request,id):
    if request.method == 'GET':
        forms = Awards.objects.all()
    return render(request, 'view_awards.html',{'forms':forms})


def award_template_index(request):
	if request.method == 'GET':
		forms = Awards.objects.all()
		id = request.GET.get('id')
		load_templates = AwardTemplate.objects.all()
	return render(request, 'award_template_index.html',{'forms': forms,
        'load_templates': load_templates,
    })

def award_template_load(request,id):
	load_templates = AwardTemplate.objects.filter(award_id=id)
	to_json = serializers.serialize('json', load_templates)
	return HttpResponse(to_json, content_type='application/json')