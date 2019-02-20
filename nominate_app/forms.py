from .models import Awards, NominationPeriod
from django import forms

class AwardsForm(forms.ModelForm):

	class Meta:
		model = Awards
		fields = '__all__'

class NominationPeriodForms(forms.ModelForm):

	class Meta:
		model = NominationPeriod
		fields = '__all__'