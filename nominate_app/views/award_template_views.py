from django.shortcuts import render, redirect 
from django.forms import modelformset_factory, inlineformset_factory
from nominate_app.forms import TemplateForm, AwardQuestionForm, AwardTemplateForm, QuestionForm 
from nominate_app.models import Questions, AwardTemplate, Awards
from django.http import HttpResponse
import json
import pdb

# Create your views here.

def new_award_template(request,award_id):
    award = AwardTemplate()
    award_form = TemplateForm(instance=award)

    TemplateFormset = inlineformset_factory(AwardTemplate, Questions, form=AwardQuestionForm, extra=1)
    formset = TemplateFormset(instance=award)

    if request.method == 'POST':
        x = request.POST.copy()
        x['award'] = award_id
        request.POST = x
        award_form = TemplateForm(request.POST)
        formset = TemplateFormset(request.POST)
        if award_form.is_valid():
            created_award = award_form.save(commit=False)
            formset = TemplateFormset(request.POST, instance=created_award)

            if formset.is_valid():
                created_award.save()
                formset.save()
                return redirect('nominate_app:award_template_index')

    return render(request, 'nominate_app/new_award_template.html', {'formset':formset,'award_form':award_form })

def edit_award_template(request, template_id):
  award_template = AwardTemplate.objects.get(id = template_id)
  questions = Questions.objects.filter(award_template_id=award_template.id)
  if questions.exists():
    x=0
  else:
    x=1
  AwardTemplateFormset = modelformset_factory(Questions, fields=('qname', 'qtype', 'role', 'attachment_need'), extra=x, can_delete=True)
  if request.method == 'POST':
    # This code to be refactored. Replace with 2 forms
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
