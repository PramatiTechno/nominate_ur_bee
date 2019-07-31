from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from nominate_app.models import User, UserProfile, Nomination,Awards, AwardTemplate,NominationInstance,Group, NominationPeriod
from dateutil.relativedelta import *
from datetime import datetime
from IPython import embed

logger = get_task_logger(__name__)

@periodic_task(
  run_every=(crontab(minute='*/1')),
  name="populate_monthly_frequency",
  ignore_result=True
)

def populate_monthly_frequency(): 
	awards = Awards.objects.all()
	for award in awards: 
		award_templates = award.awardtemplate_set.all()
		periods = award.nominationperiod_set.all()
		frequency = award.frequency
		for period in periods:
			for template in award_templates:
				day,month = period.start_day.day,period.start_day.month
				if template.nomination_set.count() == 0:
					new_instance = Nomination(award_template_id= template.id,start_day=period.start_day,end_day=period.end_day,group=period.group)
					new_instance.save()
				else:
					last_nomination = template.nomination_set.last()
					next_nomination_starts_at = last_nomination.start_day 
					new_instance = Nomination(award_template_id= template.id,start_day=last_nomination.start_day,end_day=last_nomination.end_day,group=period.group)
					new_instance.save()

				    
	