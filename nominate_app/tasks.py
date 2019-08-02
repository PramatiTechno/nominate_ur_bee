from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from nominate_app.models import User, UserProfile, Nomination,Awards, AwardTemplate,NominationInstance,Group, NominationPeriod
from dateutil.relativedelta import *
from datetime import datetime,timedelta
import calendar
from IPython import embed

logger = get_task_logger(__name__)

#to start celery use 2 commands in two terminals one for worker other one for celery process
#celery -A nominate_your_bee beat -l info
#celery -A nominate_your_bee worker -l info

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime(year, month, day)

@periodic_task(
  run_every=(crontab(minute='*/1')),
  name="populate_monthly_frequency",
  ignore_result=True
)
def populate_monthly_frequency(): 
	print("Starting the script from the console")
	frequencies = {'YEARLY': 12,'MONTHLY': 1,'QUATERLY': 3}
	awards = Awards.objects.all()
	for award in awards: 
		print("Checking awards");
		award_templates = award.awardtemplate_set.all()
		periods = award.nominationperiod_set.all()
		frequency = award.frequency
		for period in periods:
			print("Iterating the periods");
			for template in award_templates:
				print("Iterating the templates");
				day,month = period.start_day.day,period.start_day.month
				group_nominations = template.nomination_set.filter(group=period.group)
				if  group_nominations.count() == 0:
					print("Group count is zero");
					if period.start_day == (datetime.now() + timedelta(hours=24)).date():
						new_instance = Nomination.objects.get_or_create(award_template_id= template.id,start_day=period.start_day,end_day=period.end_day,group=period.group)
				else:
					for nom in group_nominations:
						print("Iterating the noms");
						last_nomination = template.nomination_set.last()
						next_nomination_starts_at = add_months(last_nomination.start_day,frequencies[frequency]) 
						next_nomination_ends_at = add_months(last_nomination.end_day,frequencies[frequency])
						if next_nomination_starts_at == (datetime.now() + timedelta(hours=24)).date():
							new_instance = Nomination.objects.get_or_create(award_template_id=template.id,start_day=next_nomination_starts_at,end_day=next_nomination_ends_at,group=period.group)
