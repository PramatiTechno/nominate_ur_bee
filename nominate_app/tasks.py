from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from nominate_app.models import User, UserProfile, \
Nomination,Awards, AwardTemplate,NominationInstance,Group, NominationPeriod
from dateutil.relativedelta import *
from datetime import datetime,timedelta
import calendar
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from IPython import embed

logger = get_task_logger(__name__)

#to start celery use 2 commands in two terminals one for worker other one for celery process
#celery -A nominate_your_bee beat -l info
#celery -A nominate_your_bee beat --detach -l info -f beat.log

#celery -A nominate_your_bee worker --detach -l info -f worker.log


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime(year, month, day)

def sending(values, nom_obj, template_name, subject):
    for index, value in enumerate(values):
        print(value.email)
        print(value.username)
        context = {str(nom_obj[index].group.name)+'_name':value, 
        'start_date':nom_obj[index].start_day, 'last_date':nom_obj[index].end_day}
        message_value_html_template = render_to_string(template_name, context=context)
        plain_message_value = strip_tags(message_value_html_template)
        print('message----->>>',plain_message_value)
        # send_mail(subject=subject, from_email='no-reply@pramati.com', recipient_list=[str(value)], message=plain_message_value, fail_silently=False)
        print('mail sent to ' + str(value))
    return 'mail sent'
managers_start_sent = False
managers_updated_sent = False
managers_end_sent = False
tech_jury_start_sent = False
tech_jury_updated_sent = False
tech_jury_end_sent = False
director_start_sent = False
director_updated_sent = False
director_end_sent = False


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


@periodic_task(run_every=(crontab(minute='*/1')), name="email_task", ignore_result=True)
def email_task():
	# subjects
    manager_start_date = "its time to nominate your bee"
    manager_end_date = "Reminder : Just few more days to nominate you bee"
    manager_extension_date = "Extended !!!"
    tech_jury_start_date = "its time to submit review submission"
    tech_jury_extension_date = "Extended !!!"
    tech_jury_end_date = "Reminder: Just a few more days to submit your reviews"
    director_start_date = "Its time to start reviews submission"
    director_extension_date = "Extended !!!"
    director_end_date = "Reminder: Just a few more days to submit your reviews"
	# from
    from_email = settings.EMAIL_HOST_USER
	# to
    to_admin = User.objects.filter(groups__name='Admin')
    to_manager = User.objects.filter(groups__name='Manager')
    to_tech_jury = User.objects.filter(groups__name='Technical Jury Member')
    to_director = User.objects.filter(groups__name='Directorial Board Member')
    nominations_admin = Nomination.objects.filter(group__name='Admin')
    nominations_manager = Nomination.objects.filter(group__name='Manager')
    nominations_tech_jury = Nomination.objects.filter(group__name='Technical Jury Member')
    nominations_director = Nomination.objects.filter(group__name='Directorial Board Member')
    if nominations_manager:
        if nominations_manager.filter(start_day=(datetime.today()+ timedelta(hours=24)).date()):
            global managers_start_sent
            if managers_start_sent == False:
                sending(to_manager, nominations_manager, 'nominate_app/emails/managers_start-date.html', manager_start_date)
                managers_start_sent = True
        else: managers_start_sent == False
        if nominations_manager.filter(end_day=(datetime.today()+ timedelta(hours=72)).date()):
            global managers_end_sent
            if managers_end_sent == False:
                sending(to_manager, nominations_manager, 'nominate_app/emails/managers_end-date.html', manager_end_date)
                managers_end_sent == True
        else: managers_end_sent = False
        if nominations_manager.filter(updated_at=(datetime.today())):
            global managers_updated_sent
            if managers_updated_sent == False:
                sending(to_manager, nominations_manager, 'nominate_app/emails/managers_extension.html', manager_extension_date)
                managers_updated_sent = True
        else: managers_updated_sent = False
    elif nominations_tech_jury:
        if nominations_tech_jury.filter(start_day=(datetime.today()+ timedelta(hours=24)).date()):
            global tech_jury_start_sent
            if tech_jury_start_sent == False:
                sending(to_tech_jury, nominations_tech_jury, 'nominate_app/emails/tech_jury_start-date.html', tech_jury_start_date)
                tech_jury_start_sent = True
        else:tech_jury_start_sent = False
        if nominations_tech_jury.filter(end_day=(datetime.today()+ timedelta(hours=72)).date()):
            global tech_jury_end_sent
            if tech_jury_end_sent == False:
                sending(to_tech_jury, nominations_tech_jury, 'nominate_app/emails/tech_jury_end-date.html', tech_jury_end_date)
                tech_jury_end_sent = True
        else: tech_jury_end_sent = False
        if nominations_tech_jury.filter(updated_at=(datetime.today())):
            global tech_jury_updated_sent
            if tech_jury_updated_sent == False:
                sending(to_tech_jury, nominations_tech_jury, 'nominate_app/emails/tech_jurys_extension_extension.html', tech_jury_extension_date)
                tech_jury_updated_sent = True
        else: tech_jury_updated_sent = False
    elif nominations_director:
        if nominations_director.filter(start_day=(datetime.today()+ timedelta(hours=24)).date()):
            global director_start_sent
            if director_start_sent == False:
                sending(to_director, nominations_director, 'nominate_app/emails/directors_start-date.html', director_start_date)
                director_start_sent = True
        else:director_start_sent = False
        if nominations_director.filter(end_day=(datetime.today()+ timedelta(hours=72)).date()):
            global director_end_sent
            if director_end_sent == False:
                sending(to_director, nominations_director, 'nominate_app/emails/directors_end-date.html', director_start_date)
                director_end_sent = True
        else: director_end_sent = False
        if nominations_director.filter(updated_at=(datetime.today())):
            global director_updated_sent
            if director_updated_sent == False:
                sending(to_director, nominations_director, 'nominate_app/emails/directors_extension.html', director_extension_date)
                tech_jury_updated_sent = True
        else: tech_jury_updated_sent = False
        