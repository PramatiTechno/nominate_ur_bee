from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(models.Model):
	name = models.CharField(max_length=30)
	email = models.EmailField(max_length=70, unique=True)
	designation = models.CharField(max_length=70)

	def __str__(self):
		return self.name

class Role(models.Model):
	LEVEL1 = 'l1'
	LEVEL2 = 'l2'
	LEVEL3 = 'l3'

	choice_level = (
		(LEVEL1, 'level1'),
		(LEVEL2, 'level2'),
		(LEVEL3, 'level3'),
		)

	name = models.CharField(max_length=30)
	group = models.CharField(choices=choice_level, max_length=3)

	def __str__(self):
		return self.group

class User_Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_role'

class Awards(models.Model):
	MONTHLY = 'M'
	QUATERLY = 'Q'
	YEARLY = 'Y'

	choice_type = (
		(MONTHLY, 'Monthly'),
		(QUATERLY, 'Quaterly'),
		(YEARLY, 'Yearly')
		)

	name = models.CharField(max_length=30, null=True, blank=True)
	is_active = models.BooleanField(default = False)
	frequency = models.CharField(max_length=3, choices=choice_type)
	description = models.CharField(max_length=200, null=True, blank=True)
	# get_awardtype_display()

	def __str__(self):
		return self.name

class NominationPeriod(models.Model):
	level = models.ForeignKey(Role, on_delete=models.CASCADE)
	award = models.ForeignKey(Awards, on_delete=models.CASCADE)
	start_day = models.IntegerField(choices=list(range(1, 31)))
	end_day = models.IntegerField(choices=list(range(1, 31)))

	
class AwardTemplate(models.Model):
	template_name = models.CharField(max_length=30, null=True, blank=True)
	award = models.ForeignKey(Awards, on_delete=models.CASCADE)

	def __str__(self):
		return self.template_name


class Questions(models.Model):
	SUBJECTIVE = 'S'
	OBJECTIVE = 'O'

	query_choice = (
		(SUBJECTIVE, 'subjective'),
		(OBJECTIVE, 'objective')
		)

	qname = models.CharField(max_length=100)
	qtype = models.CharField(max_length=1, choices=query_choice)
	award_template = models.ForeignKey(AwardTemplate, on_delete=models.CASCADE)
	role = models.ForeignKey(Role, on_delete=models.CASCADE)
	attachment_need = models.BooleanField(default=False)

	def __str__(self):
		return self.qname
