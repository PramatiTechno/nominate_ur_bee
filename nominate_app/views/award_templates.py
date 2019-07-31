from django.shortcuts import render, redirect 
from django.forms import modelformset_factory, inlineformset_factory
from nominate_app.forms import TemplateForm, AwardQuestionForm
from nominate_app.models import Questions, AwardTemplate, Awards
from django.http import HttpResponse
from django.contrib import messages
from nominate_app.utils import group_required
from IPython import embed
from django.utils import timezone
import json
 
@group_required('Admin', raise_exception=True)
def home(request):
  if Awards.objects.count()==0:
    awards=[]
    templates=[]
    award = Awards()
  else:
    awards = Awards.objects.all().order_by('id')
    award = Awards.objects.first()
    try: 
      templates = AwardTemplate.objects.filter(award_id=award.id) 
    except AwardTemplate.DoesNotExist:
      templates = [] 
  return render(request, 'nominate_app/award_templates/index.html',{'award': award,'forms': awards,
    'load_templates': templates
  })

def index(request,award_id):
  if request.method == 'GET':
    if Awards.objects.count()==0:
      awards=[]
      award = Awards()
      templates=[]
    else:
      awards = Awards.objects.all().order_by('id')
      award = Awards.objects.get(id=award_id)
      try: 
        templates = AwardTemplate.objects.filter(award_id=award.id) 
      except AwardTemplate.DoesNotExist:
        templates = [] 
    return render(request, 'nominate_app/award_templates/index.html',{'award': award,'forms': awards,
      'load_templates': templates
    })
  elif request.method == 'POST':
    award_template = AwardTemplate()
    award_form = TemplateForm(instance=award_template)
    TemplateFormset = inlineformset_factory(AwardTemplate, Questions, form=AwardQuestionForm, extra=1)
    formset = TemplateFormset(instance=award_template)
    x = request.POST.copy()
    x['award'] = award_id
    request.POST = x
    award_form = TemplateForm(request.POST)
    formset = TemplateFormset(request.POST)
    if award_form.is_valid():
      if formset.is_valid():
        award = Awards.objects.get(id=award_id)
        content = request.POST
        created_award = award_form.save()
        for i in range(int(content['questions_set-TOTAL_FORMS'])):
          qtype = content['questions_set-{0}-qtype'.format(i)]
          if qtype == "SUBJECTIVE":
            question = Questions(qname=content['questions_set-{0}-qname'.format(i)], qtype=qtype, \
            attachment_need=False, created_at=timezone.now(), award_template_id = created_award.id, \
            group_id=content['questions_set-{0}-group'.format(i)])
            question.save()
          else:
            question = Questions(qname=content['questions_set-{0}-qname'.format(i)], qtype=qtype, \
            attachment_need=False, created_at=timezone.now(), award_template_id = created_award.id, \
            group_id=content['questions_set-{0}-group'.format(i)], options=content.getlist('questions_set-{0}-objectives'.format(i)))
            question.save()
          messages.success(request, 'Award Template created successfully.')
        return redirect('nominate_app:award_templates_index', award_id=award.id)

def new(request,award_id):
  award_template = AwardTemplate()
  award_form = TemplateForm(instance=award_template)
  TemplateFormset = inlineformset_factory(AwardTemplate, Questions, form=AwardQuestionForm, extra=1)
  formset = TemplateFormset(instance=award_template)
  award = Awards.objects.get(id=award_id)
  return render(request, 'nominate_app/award_templates/new.html', {'formset':formset,'award_form':award_form,'award': award })

def edit(request,award_id,award_template_id):
  award = Awards.objects.get(id=award_id)
  award_template = AwardTemplate.objects.get(id = award_template_id)
  template_form = TemplateForm(instance=award_template)
  questions = Questions.objects.filter(award_template_id=award_template.id)
  if questions.exists():
    x=0
  else:
    x=1
  TemplateFormset = inlineformset_factory(AwardTemplate, Questions, form=AwardQuestionForm, extra=x)
  formset = TemplateFormset(instance=award_template,queryset=questions)
  return render(request, 'nominate_app/award_templates/edit.html', {'formset':formset,'template_form':template_form,'award': award,'award_template': award_template })

 
@group_required('Admin', raise_exception=True)
def award_template(request,award_id,award_template_id):
    method = request.POST.get('_method', '').lower()
    award = Awards.objects.get(id=award_id) 
    try:
      award_template = AwardTemplate.objects.get(id=award_template_id) 
    except AwardTemplate.DoesNotExist:
      messages.success(request, 'Award Template does not exist')
      return redirect('nominate_app:award_templates') 
    if request.method == 'GET':
      return render(request, 'nominate_app/award_templates/show.html', {'award':award })
    elif method == 'put': 
      award_template = AwardTemplate.objects.get(id = award_template_id)
      template_form = TemplateForm(instance=award_template)
      questions = Questions.objects.filter(award_template_id=award_template.id)
      if questions.exists():
        x=0
      else:
        x=1
      TemplateFormset = inlineformset_factory(AwardTemplate, Questions, form=AwardQuestionForm, extra=x)
      formset = TemplateFormset(instance=award_template,queryset=questions)
      new_form = request.POST.copy()
      new_form['award'] = str(award_template.award_id)
      request.POST = new_form
      is_active = request.POST.get('is_active',False)
      if is_active == 'on':
        is_active = True
      template_form = TemplateForm(request.POST)
      formset = TemplateFormset(request.POST)
      if template_form.is_valid():
        created_award = AwardTemplate.objects.filter(id=award_template_id).update(template_name= new_form['template_name'], is_active=is_active)
        formset = TemplateFormset(request.POST, instance=award_template)
        if formset.is_valid():
          formset.save()
          messages.success(request, 'Award Template is updated successfully.')
          return redirect('nominate_app:award_templates_index', award_id=award.id)
    elif method == 'delete':
      if award_template.delete():
         messages.success(request, 'Award is deleted successfully')
         return redirect('nominate_app:award_templates_index', award_id=award.id)
      else:
         messages.success(request, 'Could not delete award. Contact Admin')
         return redirect('nominate_app:award_templates_index', award_id=award.id)

      