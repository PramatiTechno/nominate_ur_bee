from django import forms  
from nominate_app.models import Awards, NominationPeriod, AwardTemplate, Questions
from django.forms import inlineformset_factory
class AwardTemplateForm(forms.ModelForm): 
    class Meta:
        model = AwardTemplate  
        fields = "__all__"

class QuestionForm(forms.ModelForm):  
    class Meta:
        model = Questions  
        fields = "__all__"  

class AwardsForm(forms.ModelForm):

	class Meta:
		model = Awards
		fields = ('name', 'frequency', 'description', 'is_active')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class': 'form-control def', 'placeholder': "Enter Award Name"})
		self.fields['frequency'].widget.attrs.update({'class': 'form-control abc'})
		self.fields['description'].widget.attrs.update({'class': 'form-control ghi', 'placeholder': "what's this award for ??"})
	        



class AwardsActiveForm(forms.ModelForm):

    class Meta:
        model = Awards
        fields = ('is_active',)


class NominationPeriodForm(forms.ModelForm):

	class Meta:
		model = NominationPeriod
		fields = ('level', 'start_day', 'end_day')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['level'].widget.attrs.update({'class': 'form-control abc'})
		self.fields['start_day'].widget.attrs.update({'class': 'form-control def'})
		self.fields['end_day'].widget.attrs.update({'class': 'form-control ghi'})