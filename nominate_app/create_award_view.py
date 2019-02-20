from django.shortcuts import render, redirect
from .models import NominationPeriod, Awards, Role
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponse

# Create your views here.

def home(request, award_id):
	award = Awards.objects.get(pk=award_id)
	query = NominationPeriod.objects.filter(award_id=award.id)
	if query.exists():
		x=0
	else:
		x=1
	NominationFormset = modelformset_factory(NominationPeriod, fields=('level', 'start_day', 'end_day'), extra=x, can_delete=True)
	if request.method == 'POST':
		formset = NominationFormset(request.POST, queryset=query)
		if formset.is_valid():
			instances = formset.save(commit=False)
			for instance in instances:
				instance.award_id=award.id
				instance.save()
			return redirect('home', award_id=award.id)

	else:
		formset = NominationFormset(queryset=query)

	return render(request, 'home.html', {'formset':formset})

def award_delete(request, nom_id):
	NominationPeriod.objects.get(pk=nom_id).delete()
	return HttpResponse('')