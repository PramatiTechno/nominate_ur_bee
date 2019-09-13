from django.shortcuts import render, redirect 
from django.forms import modelformset_factory, inlineformset_factory
from nominate_app.forms import TemplateForm, AwardQuestionForm
from nominate_app.models import Questions, AwardTemplate, Awards
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.contrib import messages
from nominate_app.utils import group_required
from IPython import embed
from django.utils import timezone
from functools import partial, wraps
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
          attachment_needed = bool(content['questions_set-{0}-attachment_need'.format(i)]) if 'questions_set-{0}-attachment_need'.format(i) in content else False
          if qtype == "SUBJECTIVE":
            question = Questions(qname=content['questions_set-{0}-qname'.format(i)], qtype=qtype, \
            attachment_need=attachment_needed, created_at=timezone.now(), award_template_id = created_award.id)
          else:
            question = Questions(qname=content['questions_set-{0}-qname'.format(i)], qtype=qtype, \
            attachment_need=attachment_needed, created_at=timezone.now(), award_template_id = created_award.id, options=content.getlist('questions_set-{0}-objectives'.format(i)))
            
          question.save()
          groups = content.getlist('questions_set-0-group')
          for group_id in groups:
            group = Group.objects.get(id=group_id)
            question.groups.add(group)

          question.save()

          messages.success(request, 'Award Template is created successfully.')
        return redirect('nominate_app:award_templates_index', award_id=award.id)
    else:
        for field, err in award_form.errors.items():
            messages.error(request,str(err[0]))
        return render(request, 'nominate_app/award_templates/new.html', {'formset':formset,'award_form':award_form, 'frequencies': Awards.frequencies.items()})       

def new(request,award_id):
  award_template = AwardTemplate()
  award_form = TemplateForm(instance=award_template)
  
  TemplateFormset = inlineformset_factory(AwardTemplate, Questions, form=AwardQuestionForm, extra=1)
  formset = TemplateFormset(instance=award_template, form_kwargs={'award_id': award_id})
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
    formset = TemplateFormset(instance=award_template,queryset=questions, form_kwargs={'award_id': award_id})
    return render(request, 'nominate_app/award_templates/edit.html', {'formset':formset,'template_form':template_form,'award': award,'award_template': award_template, 'questions': questions })

 
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
      questions = Questions.objects.filter(award_template_id=award_template.id)
      return render(request, 'nominate_app/award_templates/show.html', {'award':award ,'template': award_template, 'questions': questions})
    elif method == 'put':       
      award_template = AwardTemplate.objects.get(id = award_template_id)
      questions = Questions.objects.filter(award_template_id=award_template.id)
      if questions.exists():
        x=0
      else:
        x=1
      new_form = request.POST.copy()
      new_form['award'] = str(award_template.award_id)
      request.POST = new_form
      is_active = request.POST.get('is_active',False)
      if is_active == 'on':
        is_active = True
      created_award = AwardTemplate.objects.filter(id=award_template_id).update(template_name= new_form['template_name'], is_active=is_active)
      content = request.POST
      prev_qids = [ question.id for question in questions ]
      for i in range(int(content['questions_set-TOTAL_FORMS'])):
        qtype = content['questions_set-{0}-qtype'.format(i)]
        qid = content.get('questions_set-{0}-id'.format(i), None)
        groups = content.getlist('questions_set-{0}-group'.format(i))
        attachment_needed = bool(content['questions_set-{0}-attachment_need'.format(i)]) if 'questions_set-{0}-attachment_need'.format(i) in content else False
        if qid:
          qid = int(qid)
          prev_qids.remove(qid)
          question = Questions.objects.get(id=qid)
          question.qname = content['questions_set-{0}-qname'.format(i)]
          question.attachment_need = attachment_needed
          question.updated_at = timezone.now()
          if qtype == "SUBJECTIVE":
            question.qtype = "SUBJECTIVE"
            question.options = None
          else:
            question.qtype = qtype
            question.options = content.getlist('questions_set-{0}-objectives'.format(qid))
          question.groups.clear()
          question.save()

          for group_id in groups:
            group = Group.objects.get(id=group_id)
            question.groups.add(group)

          question.save()

        else:
          question = Questions(qname=content['questions_set-{0}-qname'.format(i)], qtype=content['questions_set-{0}-qtype'.format(i)], attachment_need=attachment_needed, options=content.getlist('questions_set-{0}-objectives'.format(i)), created_at=timezone.now(),award_template_id=award_template_id, updated_at=timezone.now())
          question.save()
          for group_id in groups:
            group = Group.objects.get(id=group_id)
            question.groups.add(group)

          question.save()

      for pqid in prev_qids:
        deleted_question = Questions.objects.get(id=pqid)
        deleted_question.delete()

        messages.success(request, 'Award Template is updated successfully.')
      return redirect('nominate_app:award_templates_index', award_id=award.id)
    elif method == 'delete':

      if award_template.delete():
         messages.success(request, 'Award Template is deleted successfully')
         return redirect('nominate_app:award_templates_index', award_id=award.id)
      else:
         messages.success(request, 'Could not delete award. Contact Admin')
         return redirect('nominate_app:award_templates_index', award_id=award.id)

      