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
    periods = NominationPeriod.objects.filter(award=self)
    for period in periods:
      new_nomination_period = NominationPeriod.objects.get_or_create(start_day= period.start_day, end_day= period.end_day, group_id= period.group_id, award_id= period.award_id)[0]
      new_nomination_period.save()

class NominationPeriod(models.Model):
  CHOICES = [(str(i),str(i)) for i in range(1,32)]
  group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)
  award = models.ForeignKey(Awards, on_delete=models.CASCADE)
  start_day = models.DateField(max_length=20, null=False, blank=False)
  end_day = models.DateField(max_length=20, null=False, blank=False)
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
  groups = models.ManyToManyField(Group)
  attachment_need = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  options = ArrayField(models.CharField(max_length=90, blank=True), size=20,blank=True,null=True)
  deleted = models.DateTimeField(editable=False,null=True)

  def __str__(self):
    return self.qname
  # def __eq__(self, other):
  #   if self.qname == other.qname and self.qtype == other.qtype and self.options == other.options \
  #     and self.award_template_id == other.award_template_id and self.role_id == other.role_id:
  #     return True
  #   else:
  #     return False
    

class Nomination(models.Model):
  award_template = models.ForeignKey(AwardTemplate, on_delete=models.CASCADE)
  group = models.ForeignKey(Group ,on_delete=models.CASCADE)
  start_day = models.DateField(max_length=20, null=False, blank=False)
  end_day = models.DateField(max_length=20, null=False, blank=False)
  created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)

  class Meta:
    db_table='nominations'  

class DirectorComments(models.Model):
  class Meta:
    db_table='director_comment'
  comment = models.CharField(max_length=200, null=False)
  nomination_submitted = models.ForeignKey('NominationSubmitted', on_delete=models.CASCADE, related_name='director_comment')
  submitted_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='director_comment')

class NominationSubmitted(models.Model):
  class Meta:
    db_table='nomination_submitted'
  statuses = (
    ("Submitted", 0),
    ("Reviewed", 1),
    ("Approved", 2),
    ("Dismissed", 3),
    ("On hold", 4),
    )
  nomination = models.ForeignKey('Nomination', related_name='submissions', on_delete=models.SET_NULL, blank=True, null=True,)
  status = models.IntegerField(null=False, blank=False,choices=statuses,default=0)
  submitted_at = models.DateTimeField(auto_now_add=True, null=False, blank=False) 
  email = models.CharField(max_length=50, null=False, blank=False)
  firstname = models.CharField(max_length=30, null=False, blank=False)
  group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)
  designation = models.CharField(max_length=30, null=False, default="")
  lastname = models.CharField(max_length=30, null=False, blank=False)
  award_name = models.CharField(max_length=30, null=False, blank=False)
  worklocation = models.CharField(max_length=30, null=False, blank=False, default="")
  baselocation = models.CharField(max_length=30, null=False, blank=False, default="")
  template_name = models.CharField(max_length=150, null=False, blank=False)
  created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)

  def get_status(self, status_code):
    for status in self.statuses:
      if status[1] == status_code:
        return status[0]

class QuestionAnswers(models.Model):
  UPLOAD_TO = 'answers/images'
  class Meta:
    db_table='question_answers'
  nomination_submitted = models.ForeignKey(NominationSubmitted, on_delete=models.CASCADE, related_name='questions')
  question = models.CharField(max_length=100, null=False, blank=False)
  answer = models.CharField(max_length=500, null=True, blank=True)
  attachment_path = models.FileField(max_length=500, null=True, blank=True, upload_to = UPLOAD_TO)
  created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  
  def get_status(self, status_code):
    for status in self.statuses:
      if status[1] == status_code:
        return status[0]



class NominationInstance(models.Model):
  statuses =( 
    ("New",0),
    ("Saved", 1),
    ("Submitted", 2),
    ("Reviewed",3),
    ("Approved",4),
    ("Dismissed",5),
    ("On hold",6)
  )
  nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE, default=None)
  status = models.IntegerField(null=False, blank=False,choices=statuses,default=0)
  result = models.CharField(max_length=50, null=True, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  submitted_at = models.DateTimeField(auto_now_add=True, null=False, blank=False) 
  created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
  class Meta:
    db_table='nomination_instances'
  def get_status(self, status_code):
    for status in self.statuses:
      if status[1] == status_code:
        return status[0]

  def get_submitted_at_date(self):
        return self.submitted_at.strftime('%b %d, %Y')

class NominationAnswers(models.Model):
  UPLOAD_TO = 'answers/images'
  nomination_instance = models.ForeignKey(NominationInstance, on_delete=models.CASCADE, related_name='answers')
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

class Comment(models.Model):
    submission = models.ForeignKey('NominationSubmitted', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        db_table='nomination_comments'
    
    def format_date(self):
        if (self.created_date.date() == datetime.today().date()):
          return self.created_date.strftime("%I:%M %p")
        else:
          return self.created_date.strftime('%b %d, %Y')

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text 

class Like(models.Model):
  submission = models.ForeignKey('NominationSubmitted', on_delete=models.CASCADE, related_name='likes')
  voter = models.ForeignKey(User, on_delete=models.CASCADE)
  created_date = models.DateTimeField(default=timezone.now)

  class Meta:
    db_table='nomination_likes'

class NominationRating(models.Model):
  ratings = (
    ("null", 0),
    ("one", 1),
    ("two", 2),
    ("three", 3),
    ("four", 4),
    ("five", 5),
    )
  submission = models.ForeignKey('NominationSubmitted', on_delete=models.CASCADE, related_name='ratings')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  rating = models.IntegerField(null=False, blank=False,choices=ratings,default=0)
  review = models.TextField()
  reviewed_at = models.DateTimeField(default=timezone.now)

  class Meta:
    db_table='nomination_rating'


class UserInvite(models.Model):
  first_name = models.CharField(max_length=500, null=True, blank=True)
  last_name = models.CharField(max_length=500, null=True, blank=True)
  email = models.CharField(max_length=500, null=True, blank=True)
  group = models.ForeignKey(Group, on_delete=models.CASCADE)
  baselocation = models.CharField(max_length=500, null=True, blank=True)
  designation = models.CharField(max_length=500, null=True, blank=True)


  class Meta:
    db_table='user_invite'

