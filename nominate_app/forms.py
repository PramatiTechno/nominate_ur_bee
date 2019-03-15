from django import forms  
from nominate_app.models import Awards, NominationPeriod, AwardTemplate, Questions, NominationAnswers
from django.forms import inlineformset_factory

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
    fields = '__all__'


class NominationPeriodForm(forms.ModelForm):

  class Meta:
    model = NominationPeriod
    fields = ('level', 'start_day', 'end_day')

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['level'].empty_label = None
    self.initial['level'] = '2'
    self.fields['start_day'].widget.attrs.update({'class': 'form-control def'})
    self.fields['end_day'].widget.attrs.update({'class': 'form-control ghi'})


class TemplateForm(forms.ModelForm):

  class Meta:
    model = AwardTemplate
    fields = ('template_name', 'award', 'is_active' )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['template_name'].widget.attrs.update({'class': 'form-control def', 'placeholder': "Enter Award Template Name"})


class AwardQuestionForm(forms.ModelForm):

  class Meta:
    model = Questions
    fields = ('qname', 'qtype', 'role', 'attachment_need')

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['role'].empty_label = None
    self.initial['level'] = '2'
    self.fields['qname'].widget.attrs.update({'class': 'form-control', 'placeholder': "Enter Question"})
    self.fields['qtype'].widget.attrs.update({'class': 'form-control'})
    self.fields['role'].widget.attrs.update({'class': 'form-control'})
    self.fields['attachment_need'].widget.attrs.update({'class': 'form-control'})

class NominationAnswersForm(forms.ModelForm):

  class Meta:
    model = NominationAnswers
    attachment_path = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
