from django import forms  
from nominate_app.models import *
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


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control comment-text', 'rows':1, 'placeholder': "comment.."})
        self.fields['text'].label=''

class NominationPeriodForm(forms.ModelForm):

  class Meta:
    model = NominationPeriod
    fields = ('group', 'start_day', 'end_day')

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields['group'].empty_label = None
    choices = [choice for choice in self.fields['group'].choices]
    admin_group = Group.objects.get(name="Admin")
    choices.remove((admin_group.id, admin_group.name))
    self.fields['group'].choices = choices
    self.initial['group'] = Group.objects.get(name="Manager").id
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
    fields = ('qname', 'qtype', 'group', 'attachment_need')

  def __init__(self, *args, **kwargs):
    if "award_id" in kwargs:
      award_id = kwargs.pop('award_id')
    else:
      award_id = None
    super().__init__(*args, **kwargs)

    self.fields['group'].empty_label = None
    group_ids = [np.group_id for np in NominationPeriod.objects.filter(award_id=award_id)] 
    choices =[ choice for choice in self.fields['group'].choices ]
    temp_choices = dict(choices)
    updated_choices = []
    for group_id in group_ids:
      updated_choices.append((group_id, temp_choices[group_id]))
    self.fields['group'].choices = updated_choices
    self.initial['group'] = Group.objects.get(name="Manager").id

    self.fields['qname'].widget.attrs.update({'class': 'form-control', 'placeholder': "Enter Question"})
    if self.instance.qtype == "OBJECTIVE":
      self.initial['qtype'] = "OBJECTIVE"
    elif self.instance.qtype == "MULTIPLE-CHOICE":
      self.initial['qtype'] = "MULTIPLE-CHOICE"
    else:
      self.initial['qtype'] = "SUBJECTIVE"
    self.fields['qtype'].widget.attrs.update({'class': 'form-control objective-type'})
    self.fields['group'].widget.attrs.update({'class': 'form-control'})
    self.fields['attachment_need'].widget.attrs.update({'class': 'form-control'})

class NominationAnswersForm(forms.ModelForm):

  class Meta:
    model = NominationAnswers
    attachment_path = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
