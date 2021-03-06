from django.shortcuts import render, redirect
from nominate_app.models import NominationPeriod, Awards
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponse
from nominate_app.forms import AwardsForm, AwardsActiveForm, NominationPeriodForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from nominate_app.utils import group_required
from datetime import datetime
from IPython import embed


def static_group_dropdown(formset):
  for idx in sorted([1,2], reverse=True):
    del formset[0].fields['group'].choices[idx]  

  for idx in sorted([0,2], reverse=True):
    del formset[1].fields['group'].choices[idx]

  for idx in sorted([0,1], reverse=True):
    del formset[2].fields['group'].choices[idx]



def home(request):
    return redirect('nominate_app:dashboard')


@group_required('Admin', raise_exception=True)
def index(request):
  if request.method == 'GET':
    forms = Awards.objects.all()
    return render(request, 'nominate_app/awards/index.html',{'forms':forms})

  elif request.method == 'POST':
    award = Awards(name=request.POST['name'])
    NominationFormset = inlineformset_factory(Awards, NominationPeriod, form=NominationPeriodForm, extra=1)
    award_form = AwardsForm(request.POST)
    formset = NominationFormset(request.POST)
    
    for form_id in range(int(request.POST['nominationperiod_set-TOTAL_FORMS'])):
      start_day = datetime.strptime(request.POST['nominationperiod_set-{0}-start_day'.format(form_id)], '%m/%d/%Y')
      end_day = datetime.strptime(request.POST['nominationperiod_set-{0}-end_day'.format(form_id)], '%m/%d/%Y')
      if start_day > end_day:
        messages.error(request, "End date must be greater than start date.")
        return render(request, 'nominate_app/awards/new.html', {'formset':formset,'award_form':award_form, 'frequencies': Awards.frequencies.items()})
      
    if award_form.is_valid():
        created_award = award_form.save(commit=False)
        formset = NominationFormset(request.POST, instance=created_award)
        if formset.is_valid():  
            created_award.save()
            formset.save()
            created_award.save_nomination_period()
            messages.success(request, 'Award is created successfully.')
            return redirect('nominate_app:awards')
    else:
        for field, err in award_form.errors.items():
            messages.error(request,str(err[0])) 
        return render(request, 'nominate_app/awards/new.html', {'formset':formset,'award_form':award_form, 'frequencies': Awards.frequencies.items()})


@group_required('Admin', raise_exception=True)
def new(request):
  award = Awards()
  award_form = AwardsForm(instance=award)
  NominationFormset = inlineformset_factory(Awards, NominationPeriod, form=NominationPeriodForm, extra=3)
  formset = NominationFormset(instance=award)

  # to have only single options 
  static_group_dropdown(formset)

  return render(request, 'nominate_app/awards/new.html', {'formset':formset,'award_form':award_form, 'frequencies': Awards.frequencies.items()})


@group_required('Admin', raise_exception=True)
def edit(request,award_id):
  try: 
    award = Awards.objects.get(id=award_id) 
  except Awards.DoesNotExist:
    messages.success(request, 'Award does not exist')
    return redirect('nominate_app:awards') 
  award_form = AwardsActiveForm(instance=award)
  query = NominationPeriod.objects.filter(award_id=award.id)
  if query.exists():
    x=0
  else:
    x=1
  NominationFormset = inlineformset_factory(Awards, NominationPeriod, form=NominationPeriodForm, extra=x)
  formset = NominationFormset(instance=award)

  # to have only single options 
  static_group_dropdown(formset)

  return render(request, 'nominate_app/awards/edit.html', {'formset':formset, 'award':award, 'award_form':award_form, 'frequencies': Awards.edit_frequencies.items() })


@group_required('Admin', raise_exception=True)
def award(request,award_id):
    method = request.POST.get('_method', '').lower()
    try: 
      award = Awards.objects.get(id=award_id) 
    except Awards.DoesNotExist:
      messages.success(request, 'Award does not exist')
      return redirect('nominate_app:awards') 
      
    if request.method == 'GET':
      
      return render(request, 'nominate_app/awards/show.html', {'award':award })
    elif method == 'put': 
        award_form = AwardsActiveForm(request.POST, instance=award)
        query = NominationPeriod.objects.filter(award_id=award.id)
        if query.exists():
            x=0
        else:
            x=1        
        NominationFormset = inlineformset_factory(Awards, NominationPeriod, form=NominationPeriodForm, extra=x)
        formset = NominationFormset(request.POST)
        for form_id in range(int(request.POST['nominationperiod_set-TOTAL_FORMS'])):
          start_day = datetime.strptime(request.POST['nominationperiod_set-{0}-start_day'.format(form_id)], '%m/%d/%Y')
          end_day = datetime.strptime(request.POST['nominationperiod_set-{0}-end_day'.format(form_id)], '%m/%d/%Y')
          if start_day > end_day:
            messages.error(request, "End date must be greater than start date.")
            award = Awards.objects.get(id=award_id)
            return render(request, 'nominate_app/awards/edit.html', {'formset':formset, "award": award, 'award_form':award_form, 'frequencies': Awards.frequencies.items()})
        
        if award_form.is_valid():
          created_award = award_form.save(commit=False)
          formset = NominationFormset(request.POST, instance=created_award)
          if formset.is_valid():
            created_award.save()
            formset.save()
            created_award.save_nomination_period();
            messages.success(request, 'Award is updated successfully.')
            return redirect('nominate_app:awards')
    elif method == 'delete':
      
      if award.delete():
         messages.success(request, 'Award is deleted successfully')
         return redirect('nominate_app:awards')
      else:
         messages.success(request, 'Could not delete award. Contact Admin')
         return redirect('nominate_app:awards')
      