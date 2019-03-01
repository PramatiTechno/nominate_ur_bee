from django.shortcuts import render, redirect 
from django.forms import modelformset_factory, inlineformset_factory
from nominate_app.forms import TemplateForm, AwardQuestionForm, AwardTemplateForm, QuestionForm 
from nominate_app.models import Questions, AwardTemplate, Awards
from django.http import HttpResponse
from django.contrib import messages
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
                messages.success(request, 'Award Template created successfully.')
                return redirect('nominate_app:award_template_index')

    return render(request, 'nominate_app/new_award_template.html', {'formset':formset,'award_form':award_form })

def edit_award_template(request, template_id):
  award_template = AwardTemplate.objects.get(id = template_id)
  template_form = TemplateForm(instance=award_template)
  questions = Questions.objects.filter(award_template_id=award_template.id)
  if questions.exists():
    x=0
  else:
    x=1

  TemplateFormset = inlineformset_factory(AwardTemplate, Questions, form=AwardQuestionForm, extra=x)
  formset = TemplateFormset(instance=award_template,queryset=questions)

  if request.method == 'POST':
      new_form = request.POST.copy()
      new_form['award'] = str(award_template.award_id)
      request.POST = new_form
      is_active = request.POST.get('is_active',False)
      if is_active == 'on':
        is_active = True

      template_form = TemplateForm(request.POST)
      formset = TemplateFormset(request.POST)
      if template_form.is_valid():
          created_award = AwardTemplate.objects.filter(id=template_id).update(template_name= new_form['template_name'], is_active=is_active)
          formset = TemplateFormset(request.POST, instance=award_template)
          if formset.is_valid():
            formset.save()
            messages.success(request, 'Award Template is updated successfully.')
            return redirect('nominate_app:award_template_index')

  else:
    formset = TemplateFormset(instance=award_template,queryset=questions)

  return render(request, 'nominate_app/edit_award_template.html', {'formset':formset,'template_form':template_form })

def delete_award_template(request, ques_id):
  questions = Questions.objects.filter(id=ques_id)
  if questions.exists():
    questions.delete()
  return HttpResponse('')
