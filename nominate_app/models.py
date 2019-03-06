from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(models.Model):
  name = models.CharField(max_length=30)
  email = models.EmailField(max_length=70, unique=True)
  designation = models.CharField(max_length=70)

  class Meta:
      db_table='users'

  def __str__(self):
      return self.name

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

class User_Role(models.Model):
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
    # get_awardtype_display()

  class Meta:
      db_table='awards'

  def __str__(self):
      return self.name


class NominationPeriod(models.Model):
  CHOICES = [(str(i),str(i)) for i in range(1,32)]
  level = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, blank=False)
  award = models.ForeignKey(Awards, on_delete=models.CASCADE)
  start_day = models.CharField(max_length=3, choices=CHOICES, null=False, blank=False, default=1)
  end_day = models.CharField(max_length=3, choices=CHOICES, null=False, blank=False, default=1)

  class Meta:
      db_table='nomination_periods'
  
class AwardTemplate(models.Model):
  template_name = models.CharField(max_length=150, null=False, blank=False)
  award = models.ForeignKey(Awards, on_delete=models.CASCADE)
  is_active = models.BooleanField(default = False)

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

  def __str__(self):
      return self.qname

class NominationPlan(models.Model):
  level = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, blank=False)
  nomination_period = models.ForeignKey(NominationPeriod, on_delete=models.CASCADE)
  start_date = models.DateField(max_length=20, null=False, blank=False)
  end_date = models.DateField(max_length=20, null=False, blank=False)

  class Meta:
      db_table='nomination_plans'

class NominationInstance(models.Model):
  nomination_plan = models.ForeignKey(NominationPlan, on_delete=models.CASCADE)
  award_template = models.ForeignKey(AwardTemplate, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  status = models.CharField(max_length=50, null=False, blank=False, default='new')
  result = models.CharField(max_length=50, null=True, blank=True)

  class Meta:
      db_table='nomination_instances'

class NominationChain(models.Model):
  nomination_instance = models.ForeignKey(NominationInstance, on_delete=models.CASCADE)
  reviewer_id = models.ForeignKey(User, on_delete=models.CASCADE)
  reviewed_at = models.DateField(max_length=20)

  class Meta:
      db_table='nomination_chains'
