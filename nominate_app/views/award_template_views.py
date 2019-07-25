from django.shortcuts import render, redirect 
from django.forms import modelformset_factory, inlineformset_factory
from nominate_app.forms import TemplateForm, AwardQuestionForm
from nominate_app.models import Questions, AwardTemplate, Awards
from django.http import HttpResponse
from django.contrib import messages
from nominate_app.utils import group_required
import json
from IPython import embed
from django.utils import timezone


# Create your views here.
def home(request):
  if request.user.groups.filter(name="Admin").exists():
    return redirect('nominate_app:awards')
  else:
    return redirect('nominate_app:manager_nominate_index')

@group_required('Admin', raise_exception=True)
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
      if formset.is_valid():
        content = request.POST
        created_award = award_form.save()
        for i in range(int(content['questions_set-TOTAL_FORMS'])):
          qtype = content['questions_set-{0}-qtype'.format(i)]
          if qtype == "SUBJECTIVE":
            question = Questions(qname=content['questions_set-{0}-qname'.format(i)], qtype=qtype, \
            attachment_need=False, created_at=timezone.now(), award_template_id = created_award.id, \
            role_id=content['questions_set-{0}-role'.format(i)])
            question.save()
          else:
            question = Questions(qname=content['questions_set-{0}-qname'.format(i)], qtype=qtype, \
            attachment_need=False, created_at=timezone.now(), award_template_id = created_award.id, \
            role_id=content['questions_set-{0}-role'.format(i)], options=content.getlist('questions_set-{0}-objectives'.format(i)))
            question.save()
          messages.success(request, 'Award Template created successfully.')
        return redirect('nominate_app:award_template_index')
  return render(request, 'nominate_app/new_award_template.html', {'formset':formset,'award_form':award_form })

@group_required('Admin', raise_exception=True)
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

@group_required('Admin', raise_exception=True)
def delete_award_template(request, ques_id):
  questions = Questions.objects.filter(id=ques_id)
  if questions.exists():
    questions.delete()
  return HttpResponse('')
