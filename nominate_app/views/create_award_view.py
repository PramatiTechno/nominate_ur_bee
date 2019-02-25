from django.shortcuts import render, redirect
from nominate_app.models import NominationPeriod, Awards, Role
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponse
from nominate_app.forms import AwardsForm, AwardsActiveForm, NominationPeriodForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.

def edit_awards(request, award_id):
    award = Awards.objects.get(pk=award_id)
    award_form = AwardsActiveForm(instance=award)

    query = NominationPeriod.objects.filter(award_id=award.id)
    if query.exists():
        x=0
    else:
        x=1
    NominationFormset = inlineformset_factory(Awards, NominationPeriod, fields='__all__', extra=x)
    formset = NominationFormset(instance=award)

    if request.method == 'POST':
        award_form = AwardsActiveForm(request.POST, instance=award)

        formset = NominationFormset(request.POST)

        if award_form.is_valid():
            created_award = award_form.save(commit=False)
            formset = NominationFormset(request.POST, instance=created_award)

            if formset.is_valid():
                created_award.save()
                formset.save()
                return redirect('nominate_app:edit_awards', award_id=award.id)

    return render(request, 'nominate_app/home.html', {'formset':formset, 'award':award, 'award_form':award_form })


def award_delete(request, nom_id):
    NominationPeriod.objects.get(pk=nom_id).delete()
    return HttpResponse('')

def awards(request):
    award = Awards()
    award_form = AwardsForm(instance=award)

    NominationFormset = inlineformset_factory(Awards, NominationPeriod, form=NominationPeriodForm, extra=1)
    formset = NominationFormset(instance=award)

    if request.method == 'POST':
        award_form = AwardsForm(request.POST)

        formset = NominationFormset(request.POST)
        if award_form.is_valid():
            created_award = award_form.save(commit=False)
            formset = NominationFormset(request.POST, instance=created_award)

            if formset.is_valid():
                created_award.save()
                formset.save()
                return redirect('nominate_app:view_awards')

    return render(request, 'nominate_app/awards_form.html', {'formset':formset,'award_form':award_form })

def award_delete(request, nom_id):
    NominationPeriod.objects.get(pk=nom_id).delete()
    return HttpResponse('')