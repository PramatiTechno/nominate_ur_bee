from django.shortcuts import render, redirect 
from django.forms import modelformset_factory
from nominate_app.forms import AwardTemplateForm, QuestionForm 
from nominate_app.models import Questions, AwardTemplate, Awards
from django.http import HttpResponse
import json
import pdb

# Create your views here.
def new_home(request):
  return render(request, 'new_home.html')

def new_award_template(request):
  AwardTemplateFormset = modelformset_factory(Questions, fields=('qname', 'qtype', 'role', 'attachment_need'), extra=1, can_delete=True)
  if request.method == 'POST':
    new_form = request.POST.copy()
    template_name = new_form.pop('template_name')[0]
    is_active_val = new_form.pop('is_active')[0] 
    is_active = True if is_active_val ==  'yes' else False
    award_id = new_form.pop('award_id')[0]
    award_template = AwardTemplate.objects.create(template_name= template_name, is_active=is_active, award_id=award_id)
    request.POST = new_form
    formset = AwardTemplateFormset(request.POST)
    if formset.is_valid():
      instances = formset.save(commit=False)
      for obj in formset.deleted_objects:
        obj.delete()
      for instance in instances:
        instance.award_template_id=award_template.id
        instance.save()
      return redirect('new_home')

  else:
    formset = AwardTemplateFormset(queryset=Questions.objects.none())

  return render(request, 'new_award_template.html', {'formset':formset})

def edit_award_template(request, award_template_id):
  award_template = AwardTemplate.objects.get(id = award_template_id)
  questions = Questions.objects.filter(award_template_id=award_template.id)
  if questions.exists():
    x=0
  else:
    x=1
  AwardTemplateFormset = modelformset_factory(Questions, fields=('qname', 'qtype', 'role', 'attachment_need'), extra=x, can_delete=True)
  if request.method == 'POST':
    formset = AwardTemplateFormset(request.POST, queryset=questions)
    if formset.is_valid():
      instances = formset.save(commit=False)
      for obj in formset.deleted_objects:
        obj.delete()
      for instance in instances:
        instance.award_template_id=award_template.id
        instance.save()
      return redirect('new_home')

  else:
    formset = AwardTemplateFormset(queryset=questions)

  return render(request, 'new_award_template.html', {'formset':formset})

def delete_award_template(request, ques_id):
  question = Questions.objects.get(pk=ques_id)
  if question.exists():
    question.delete()
  return HttpResponse('')
