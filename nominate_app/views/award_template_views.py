from django.shortcuts import render, redirect 
from django.forms import modelformset_factory, inlineformset_factory
from nominate_app.forms import AwardTemplateForm, QuestionForm 
from nominate_app.models import Questions, AwardTemplate, Awards
from django.http import HttpResponse
import json
import pdb

# Create your views here.

def new_award_template(request, award_id):
  award = Awards.objects.get(id = award_id)
  award_template_form = AwardTemplateForm(instance=AwardTemplate())
  AwardTemplateFormset = inlineformset_factory(AwardTemplate, Questions, form=QuestionForm, extra=1)
  formset = AwardTemplateFormset(instance=AwardTemplate())
  if request.method == 'POST':
    new_form = request.POST.copy()
    is_active_val = new_form.pop('is_active')[0] 
    is_active = True if is_active_val ==  'yes' else False
    new_form['award'] = award.id
    request.POST = new_form
    award_template_form = AwardTemplateForm(request.POST)
    formset = AwardTemplateFormset(request.POST)
    if award_template_form.is_valid():
      award_template_obj = award_template_form.save(commit=False)
      formset = AwardTemplateFormset(request.POST, instance=award_template_obj)
      if formset.is_valid():
        award_template_obj.save()
        formset.save()
        return redirect('nominate_app:award_template_index')
      else:
        return render(request, 'nominate_app/new_award_template.html', {'formset':formset, 'template_name': award.name, 'form':award_template_form})
    else:
      return render(request, 'nominate_app/new_award_template.html', {'formset':formset, 'template_name': award.name, 'form':award_template_form})
  return render(request, 'nominate_app/new_award_template.html', {'formset':formset, 'template_name': award.name})

def edit_award_template(request, template_id):
  award_template = AwardTemplate.objects.get(id = template_id)
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
      return redirect('award_template_index')

  else:
    formset = AwardTemplateFormset(queryset=questions)

  return render(request, 'nominate_app/new_award_template.html', {'formset':formset, 'award_template': award_template})

def delete_award_template(request, ques_id):
  questions = Questions.objects.filter(id=ques_id)
  if questions.exists():
    questions.delete()
  return HttpResponse('')
