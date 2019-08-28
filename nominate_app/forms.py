from django import forms  
from nominate_app.models import *
from django.forms import inlineformset_factory
from IPython import embed

class AwardsForm(forms.ModelForm):

  class Meta:
    model = Awards
    fields = ('name', 'frequency', 'description', 'is_active')

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    if args:
      self.initial['name'] = args[0]['name']
      self.initial['frequency'] = args[0]['frequency']
    self.fields['name'].widget.attrs.update({'class': 'form-control def', 'value': "Enter Award Name"})
    self.fields['frequency'].widget.attrs.update({'class': 'form-control abc'})
    self.fields['description'].widget.attrs.update({'class': 'form-control ghi', 'placeholder': "what's this award for ??"})

class AwardsActiveForm(forms.ModelForm):

  class Meta:
    model = Awards
    fields = '__all__'


class NominationFilterForm(forms.Form):
    SORT_CHOICES = [('latest', 'Latest'), ('oldest', 'Oldest')]

    Awards = forms.ChoiceField(widget=forms.Select(attrs={'onchange':'get_templates();','class': "mySelect btn btn-info"}))
    Templates = forms.ChoiceField(widget=forms.Select(attrs={'class': "mySelect btn btn-info"}))
    Sort = forms.ChoiceField(choices=SORT_CHOICES, widget=forms.Select(attrs={'class': "mySelect btn btn-info"}))
    from_ = forms.CharField(label='From', widget=forms.TextInput(attrs={'class': "form-control datepicker", 'id': "start_date", 'name': "start_date"}))
    to = forms.CharField(label='To', widget=forms.TextInput(attrs={'class': "form-control datepicker", 'id': "end_date", 'name': "end_date"}))

    def __init__(self, *args, **kwargs):
      super(NominationFilterForm, self).__init__(*args, **kwargs)
      self.fields['from_'].required = False
      self.fields['to'].required = False
      self.fields['Awards'].choices = [('ALL', 'ALL'), ] + [(award, award) for award in NominationSubmitted.objects.values_list('award_name', flat=True).distinct()]
      self.fields['Templates'].choices = [('ALL', 'ALL'), ] + [(template, template) for template in NominationSubmitted.objects.values_list('template_name', flat=True).distinct()]


class AddUserForm(forms.ModelForm):

  class Meta:
    model = UserInvite
    fields = ['email', 'group']

  def __init__(self, *args, **kwargs):
      super(AddUserForm, self).__init__(*args, **kwargs)
      self.fields['email'].required = True
      self.fields['email'].widget.attrs.update({'class': 'form-control'})
      self.fields['group'].choices = [(group.id, group.name) for group in Group.objects.all()]
      self.fields['group'].widget.attrs.update({'class': 'form-control'})

class AddGroupForm(forms.ModelForm):

  class Meta:
    model = UserInvite
    fields = ['group']

  def __init__(self, *args, **kwargs):
    super(AddGroupForm, self).__init__(*args, **kwargs)
    self.fields['group'].choices = [(group.id, group.name) for group in Group.objects.all()]
    self.fields['group'].widget.attrs.update({'class': 'form-control'})

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
    if self.instance.group_id:
      self.initial['group'] = self.instance.group_id  
    else:
      self.initial['group'] = Group.objects.get(name="Manager").id
    if self.instance.start_day and self.instance.end_day:
      sday = self.instance.start_day
      eday = self.instance.end_day
      self.initial['start_day'] = sday.strftime('%m/%d/%Y')
      self.initial['end_day'] = eday.strftime('%m/%d/%Y')
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
    if self.instance.group_id:
      self.initial['group'] = self.instance.group_id  
    else:
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
