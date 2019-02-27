from django.shortcuts import render, redirect 
from django.forms import modelformset_factory
from nominate_app.forms import AwardTemplateForm, QuestionForm 
from nominate_app.models import Questions, AwardTemplate, Awards
from django.http import HttpResponse
import json
import pdb

# Create your views here.

def new_award_template(request, award_id):
  award = Awards.objects.get(id = award_id)
  is_active=False
  AwardTemplateFormset = modelformset_factory(Questions, fields=('qname', 'qtype', 'role', 'attachment_need'), extra=1, can_delete=True)
  if request.method == 'POST':
    new_form = request.POST.copy()
    template_name = new_form.pop('template_name')[0] 
    is_active_val = new_form.pop('is_active', ['off'])
    is_active = True if is_active_val[0] ==  'on' else False
    award_id = award.id
    if (template_name != ''):
      award_template =AwardTemplate.objects.create(template_name= template_name, is_active=is_active, award_id=award_id)
      request.POST = new_form
      formset = AwardTemplateFormset(request.POST)
      if formset.is_valid():
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
          obj.delete()
        for instance in instances:
          instance.award_template_id=award_template.id
          instance.save()
        return redirect('nominate_app:award_template_index')
    else:
      return render(request, 'nominate_app/new_award_template.html', {'formset':formset, 'template_name': award.name, 'form_errors': 'Template name is required'})
  else:
    formset = AwardTemplateFormset(queryset=Questions.objects.none())

  return render(request, 'nominate_app/new_award_template.html', {'formset':formset, 'template_name': award.name})

def edit_award_template(request, template_id):
  award_template = AwardTemplate.objects.get(id = template_id)
  questions = Questions.objects.filter(award_template_id=award_template.id)
  # pdb.set_trace()
  if questions.exists():
    x=0
  else:
    x=1
  AwardTemplateFormset = modelformset_factory(Questions, fields=('qname', 'qtype', 'role', 'attachment_need'), extra=x, can_delete=True)
  if request.method == 'POST':
    new_form = request.POST.copy()
    template_name = new_form.pop('template_name')[0] 
    is_active_val = new_form.pop('is_active', ['off'])
    is_active = True if is_active_val[0] ==  'on' else False
    request.POST = new_form
    award_template_new = AwardTemplate.objects.filter(id=template_id).update(template_name= template_name, is_active=is_active)
    formset = AwardTemplateFormset(request.POST, queryset=questions)
    if formset.is_valid():
      instances = formset.save(commit=False)
      for obj in formset.deleted_objects:
        obj.delete()
      for instance in instances:
        instance.award_template_id=award_template.id
        instance.save()
      return redirect('nominate_app:award_template_index')

  else:
    formset = AwardTemplateFormset(queryset=questions)

  return render(request, 'nominate_app/edit_award_template.html', {'formset':formset, 'award_template': award_template })

def delete_award_template(request, ques_id):
  questions = Questions.objects.filter(id=ques_id)
  if questions.exists():
    questions.delete()
  return HttpResponse('')
