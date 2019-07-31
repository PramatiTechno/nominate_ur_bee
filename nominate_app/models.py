from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, Group
from dateutil.relativedelta import *
from datetime import datetime
from IPython import embed
from django.contrib.postgres.fields import ArrayField
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE
import safedelete.managers as managers
import safedelete
# from django.contrib.auth.models import AbstractUser

# Create your models here.

Group.add_to_class('group', models.CharField(max_length=30, default='level0'))    
class SafeDeleteQuestionsManager(managers.SafeDeleteManager):
  _safedelete_visibility = safedelete.managers.DELETED_INVISIBLE

class UserProfile(models.Model):
  email = models.EmailField(max_length=70, unique=True)
  designation = models.CharField(max_length=70)
  phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
  telephonenumber = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
  employeenumber = models.CharField(max_length=70)
  jobtitle = models.CharField(max_length=70)
  cn = models.CharField(max_length=70)
  title = models.CharField(max_length=70)
  lastpwdchange = models.CharField(max_length=70)
  defaultpwd = models.CharField(max_length=70)
  baselocation = models.CharField(max_length=70)
  uid = models.CharField(max_length=70)
  worklocation = models.CharField(max_length=70)
  user = models.OneToOneField(User,on_delete=models.PROTECT)
  created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)

  class Meta:
      db_table='user_profiles'

  def __str__(self):
      return self.email

  def get_group_name(self):
    return self.user.groups.all()[0].name.lower()

class Awards(models.Model):
  choice_type = (
      ('MONTHLY', 'Monthly'),
      ('QUATERLY', 'Quaterly'),
      ('YEARLY', 'Yearly')
  )
  frequencies = {"": "Please select", "MONTHLY":"Monthly", "QUATERLY": "Quaterly", "YEARLY": "Yearly"}
  edit_frequencies = {"MONTHLY":"Monthly", "QUATERLY": "Quaterly", "YEARLY": "Yearly"}
  name = models.CharField(max_length=30, null=False, blank=False)
  is_active = models.BooleanField(default = False)
  frequency = models.CharField(max_length=10, choices=choice_type, null=False, blank=False)
  description = models.CharField(max_length=200, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)

  class Meta:
    db_table='awards'
    permissions = (
           ("award_crud", "can have all the access"),
     )

  def __str__(self):
    return self.name

  def save_nomination_period(self):
    frequencies = NominationPeriod.objects.filter(award= self)
    for frequency in frequencies:
      new_nomination_period = NominationPeriod.objects.get_or_create(start_day= frequency.start_day, end_day= frequency.end_day, level_id= frequency.level_id, award_id= frequency.award_id)[0]
      new_nomination_period.save()

class NominationPeriod(models.Model):
  CHOICES = [(str(i),str(i)) for i in range(1,32)]
  level = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)
  award = models.ForeignKey(Awards, on_delete=models.CASCADE)
  start_day = models.DateField(max_length=20, null=False, blank=False)
  end_day = models.DateField(max_length=20, null=False, blank=False)
  is_template = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)

  class Meta:
    db_table='nomination_periods'
  
class AwardTemplate(models.Model):
  template_name = models.CharField(max_length=150, null=False, blank=False)
  award = models.ForeignKey(Awards, on_delete=models.CASCADE)
  is_active = models.BooleanField(default = False)
  created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  class Meta:
    db_table='award_templates'

  def __str__(self):
    return self.template_name

class Questions(SafeDeleteModel):
  _safedelete_policy = SOFT_DELETE
  query_choice = (
      ('SUBJECTIVE', 'subjective'),
      ('OBJECTIVE', 'objective'),
      ('MULTIPLE-CHOICE', 'multiple-choice')
  )
  objects = SafeDeleteQuestionsManager()
  class Meta:
    db_table='award_questions'
    
  qname = models.CharField(max_length=100, null=False, blank=False)
  qtype = models.CharField(max_length=100, choices=query_choice, null=False, blank=False, default='subjective')
  award_template = models.ForeignKey(AwardTemplate, on_delete=models.CASCADE)
  role = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)
  attachment_need = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  options = ArrayField(models.CharField(max_length=100, blank=True), size=20,blank=True,null=True)

  def __str__(self):
    return self.qname
  # def __eq__(self, other):
  #   if self.qname == other.qname and self.qtype == other.qtype and self.options == other.options \
  #     and self.award_template_id == other.award_template_id and self.role_id == other.role_id:
  #     return True
  #   else:
  #     return False
    

class NominationInstance(models.Model):
  award_template = models.ForeignKey(AwardTemplate, on_delete=models.CASCADE)
  status = models.CharField(max_length=50, null=False, blank=False, default='new')
  result = models.CharField(max_length=50, null=True, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)

  class Meta:
    db_table='nomination_instances'

class NominationSubmitter(models.Model):
  submit_choice =( 
    ("SAVE", 1),
    ("SUBMIT", 0)
  )
  nomination_instance = models.ForeignKey(NominationInstance, on_delete=models.CASCADE)
  reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
  reviewed_at = models.DateField(max_length=20, null=True, blank=True)
  submit_later =  models.IntegerField(choices=submit_choice, default=0)
  created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)

  class Meta:
    db_table='nomination_submitters'

class NominationAnswers(models.Model):
  UPLOAD_TO = 'answers/images'
  nomination_instance = models.ForeignKey(NominationInstance, on_delete=models.CASCADE)
  nomination_chain = models.ForeignKey(NominationSubmitter, on_delete=models.CASCADE)
  award_template = models.ForeignKey(AwardTemplate, on_delete=models.CASCADE)
  question = models.ForeignKey(Questions, on_delete=models.CASCADE)
  submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
  submitted_at = models.DateTimeField(null=True, blank=True)
  answer_option = models.BooleanField(max_length=20, null=True, blank=True)
  answer_text = models.CharField(max_length=500, null=True, blank=True)
  attachment_path = models.FileField(max_length=500, null=True, blank=True, upload_to = UPLOAD_TO)
  uploaded_at = models.DateTimeField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)


  class Meta:
    db_table='nomination_answers'

class NominationTimeSlot(models.Model):
  level = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)
  award = models.ForeignKey(Awards, on_delete=models.CASCADE)
  start_day = models.DateField(max_length=20, null=False, blank=False)
  end_day = models.DateField(max_length=20, null=False, blank=False)
  nomination_instance = models.ForeignKey(NominationInstance, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  
  class Meta:
    db_table='nomination_time_slots'

class Comment(models.Model):
    nomination = models.ForeignKey('NominationInstance', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        db_table='nomination_comments'

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text       


class Like(models.Model):
  nomination = models.ForeignKey('NominationInstance', on_delete=models.CASCADE, related_name='likes')
  voter = models.ForeignKey(User, on_delete=models.CASCADE)
  created_date = models.DateTimeField(default=timezone.now)

  class Meta:
    db_table='nomination_likes'


