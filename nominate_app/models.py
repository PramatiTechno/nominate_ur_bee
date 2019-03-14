from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


# from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(models.Model):
    firstname = models.CharField(max_length=30)
    email = models.EmailField(max_length=70, unique=True)
    designation = models.CharField(max_length=70)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    telephonenumber = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    employeenumber = models.CharField(max_length=70)
    jobtitle = models.CharField(max_length=70)
    cn = models.CharField(max_length=70)
    title = models.CharField(max_length=70)
    lastpwdchange = models.CharField(max_length=70)
    lastname = models.CharField(max_length=70)
    defaultpwd = models.CharField(max_length=70)
    baselocation = models.CharField(max_length=70)
    uid = models.CharField(max_length=70)
    worklocation = models.CharField(max_length=70)
    user = models.OneToOneField(User,on_delete=models.PROTECT)

    class Meta:
        db_table='user_profiles'

    def __str__(self):
        return self.email

class Role(models.Model):
  choice_level = (
      ('level1', 'level1'),
      ('level2', 'level2'),
      ('level3', 'level3'),
  )

  name = models.CharField(max_length=30)
  group = models.CharField(choices=choice_level, max_length=7)

  class Meta:
    db_table='roles'

  def __str__(self):
    return self.group

class UserRole(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  role = models.ForeignKey(Role, on_delete=models.CASCADE)

  class Meta:
    db_table = 'user_role'

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
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

  class Meta:
    db_table='awards'

  def __str__(self):
    return self.name


class NominationPeriod(models.Model):
  CHOICES = [(str(i),str(i)) for i in range(1,32)]
  level = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, blank=False)
  award = models.ForeignKey(Awards, on_delete=models.CASCADE)
  start_day = models.DateField(max_length=20, null=False, blank=False)
  end_day = models.DateField(max_length=20, null=False, blank=False)
  is_template = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

  class Meta:
    db_table='nomination_periods'
  
class AwardTemplate(models.Model):
  template_name = models.CharField(max_length=150, null=False, blank=False)
  award = models.ForeignKey(Awards, on_delete=models.CASCADE)
  is_active = models.BooleanField(default = False)
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

  class Meta:
    db_table='award_templates'

  def __str__(self):
    return self.template_name


class Questions(models.Model):
  query_choice = (
      ('SUBJECTIVE', 'subjective'),
      ('OBJECTIVE', 'objective')
  )
  class Meta:
    db_table='award_questions'
    
  qname = models.CharField(max_length=100, null=False, blank=False)
  qtype = models.CharField(max_length=100, choices=query_choice, null=False, blank=False, default='subjective')
  award_template = models.ForeignKey(AwardTemplate, on_delete=models.CASCADE)
  role = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, blank=False)
  attachment_need = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

  def __str__(self):
    return self.qname

class NominationPlan(models.Model):
  
  level = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, blank=False)
  nomination_period = models.ForeignKey(NominationPeriod, on_delete=models.CASCADE)
  start_date = models.DateField(max_length=20, null=False, blank=False)
  end_date = models.DateField(max_length=20, null=False, blank=False)
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

  class Meta:
    db_table='nomination_plans'

class NominationInstance(models.Model):
  award_template = models.ForeignKey(AwardTemplate, on_delete=models.CASCADE)
  status = models.CharField(max_length=50, null=False, blank=False, default='new')
  result = models.CharField(max_length=50, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

  class Meta:
    db_table='nomination_instances'

class NominationSubmitter(models.Model):
  nomination_instance = models.ForeignKey(NominationInstance, on_delete=models.CASCADE)
  reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
  reviewed_at = models.DateField(max_length=20, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

  class Meta:
      db_table='nomination_chains'

class NominationAnswers(models.Model):
  UPLOAD_TO = 'answers/images'
  nomination_instance = models.ForeignKey(NominationInstance, on_delete=models.CASCADE)
  nomination_chain = models.ForeignKey(NominationSubmitter, on_delete=models.CASCADE)
  award_template = models.ForeignKey(AwardTemplate, on_delete=models.CASCADE)
  question = models.ForeignKey(Questions, on_delete=models.CASCADE)
  submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
  submitted_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  answer_option = models.BooleanField(max_length=20, null=True, blank=True)
  answer_text = models.CharField(max_length=500, null=True, blank=True)
  attachment_path = models.FileField(max_length=500, null=True, blank=True, upload_to = UPLOAD_TO)
  uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

  class Meta:
    db_table='nomination_answers'

class AnswerAttachment(models.Model):
  answer_id = models.ForeignKey(NominationAnswers, on_delete=models.CASCADE)
  attachment_path = models.FileField(upload_to='documents/', null=True, blank=True)
  uploaded_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table='answer_attachments'

class NominationPeriodFrequency(models.Model):
  level = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, blank=False)
  award = models.ForeignKey(Awards, on_delete=models.CASCADE)
  start_day = models.DateField(max_length=20, null=False, blank=False)
  end_day = models.DateField(max_length=20, null=False, blank=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table='nomination_period_frequency' 

class NominationTimeSlot(models.Model):
  level = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, blank=False)
  award = models.ForeignKey(Awards, on_delete=models.CASCADE)
  start_day = models.DateField(max_length=20, null=False, blank=False)
  end_day = models.DateField(max_length=20, null=False, blank=False)
  nomination_instance = models.ForeignKey(NominationInstance, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    db_table='nomination_time_slot'          

