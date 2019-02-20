from django import forms  
from nominate_app.models import AwardTemplate, Questions
from django.forms import inlineformset_factory
class AwardTemplateForm(forms.ModelForm): 
    class Meta:
        model = AwardTemplate  
        fields = "__all__"

class QuestionForm(forms.ModelForm):  
    class Meta:
        model = Questions  
        fields = "__all__"  