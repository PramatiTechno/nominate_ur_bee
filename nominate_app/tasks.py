from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from nominate_app.models import NominationInstance, User, NominationSubmitter, Awards, AwardTemplate, UserRole, NominationPeriodFrequency, NominationTimeSlot
from dateutil.relativedelta import *
from datetime import datetime

logger = get_task_logger(__name__)


@periodic_task(
  run_every=(crontab(minute='*/1')),
  name="populate_monthly_frequency",
  ignore_result=True
)

def populate_monthly_frequency():  
	monthly_award = Awards.objects.get(frequency= 'MONTHLY')
	monthly_template = AwardTemplate.objects.filter(award_id= monthly_award.id, is_active= True).first()
	# We can replace '#' by month to test e.g 1,2,3 etc.... 
	monthly_levels = NominationPeriodFrequency.objects.filter(start_day__month='#')
	if monthly_levels:
	  nomination_instance = NominationInstance(award_template_id= monthly_template.id)
	  nomination_instance.save() 
		for monthly_level in monthly_levels:
			if monthly_level.start_day == datetime.strptime('2019-04-01', '%Y-%m-%d').date():
				for user in User.objects.all():
					if UserRole.objects.get(user_id=user.id).role.group == monthly_level.level.group:
				    nomination_period = NominationTimeSlot(start_day= monthly_level.start_day, end_day= monthly_level.end_day, level_id= monthly_level.level_id, award_id= monthly_level.award_id, nomination_instance= nomination_instance)
				    nomination_period.save() # set created by
						nomination_submitter = NominationSubmitter(nomination_instance= nomination_instance , reviewer= user)
						nomination_submitter.save()
			# creating record for next month     
	    new_nomination_period_requency = NominationPeriodFrequency(start_day= monthly_level.start_day + relativedelta(months=+1) , end_day= monthly_level.end_day + relativedelta(months=+1), level_id= monthly_level.level_id, award_id= monthly_level.award_id)
	    new_nomination_period_requency.save()
	