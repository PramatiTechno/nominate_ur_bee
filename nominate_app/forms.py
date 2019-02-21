from .models import 
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


class AwardsActiveForm(forms.ModelForm):

    class Meta:
        model = Awards
        fields = ('is_active',)
