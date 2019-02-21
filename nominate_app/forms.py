from .models import Awards, NominationPeriod
from django.forms import modelformset_factory, inlineformset_factory
from django import forms

class AwardsForm(forms.ModelForm):

	class Meta:
		model = Awards
		fields = ('name', 'frequency', 'description', 'is_active')


class AwardsActiveForm(forms.ModelForm):

    class Meta:
        model = Awards
        fields = ('is_active',)
