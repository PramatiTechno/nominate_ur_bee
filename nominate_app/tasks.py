from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from nominate_app.models import User, UserProfile, \
Nomination,Awards, AwardTemplate,NominationInstance,Group, \
NominationPeriod, Questions, NominationTiming
from IPython import embed
from datetime import datetime,timedelta
from dateutil.relativedelta import *
import calendar
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models import F
from django.urls import reverse
import os

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



def sending(values, start_day, end_day, award_name, template_path, subject, link):

    for index, value in enumerate(values):
        print('email-'+str(value.email))
        print('award-'+ str(award_name))
        context = {
            'name': value,
            'award': award_name, 
            'start_date': start_day, 
            'last_date': end_day,
            'link': link
        }
        message_value_html_template = render_to_string(template_path, context)
        plain_message_value = strip_tags(message_value_html_template)

        send_mail(subject=subject, from_email='no-reply@pramati.com', \
            recipient_list=[str(value.email)], message=plain_message_value, html_message=message_value_html_template, fail_silently=False)
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


# @periodic_task(
#   run_every=(crontab(minute='*/1')),
#   name="populate_monthly_frequency",
#   ignore_result=True
# )
def populate_monthly_frequency():
    print("Starting the script from the console")
    frequencies = {'YEARLY': 12,'MONTHLY': 1,'QUATERLY': 3}
    awards = Awards.objects.all()#filter(is_active=True)
    for award in awards:
        print("Checking awards");
        award_templates = award.awardtemplate_set.all()##.filter#(is_active=True)
        periods = award.nominationperiod_set.all()
        submission_period = periods.get(group_id=2)
        review_period = periods.get(group_id=3)
        approval_period = periods.get(group_id=4)
        frequency = award.frequency
        for period in periods:
            print("Iterating the periods");
            for template in award_templates:
                print("Iterating the templates");
                group_nominations = template.nomination_set.filter(group=period.group)
                if  group_nominations.count() == 0:
                    print("Group count is zero");
                    if submission_period.start_day == (datetime.now() + timedelta(hours=24)).date():
                        nt,created = NominationTiming.objects.get_or_create(award_template_id= template.id,start_day=submission_period.start_day,end_day=submission_period.end_day,
                                review_start_day=review_period.start_day, review_end_day=review_period.end_day,
                                    approval_start_day=approval_period.start_day, approval_end_day=approval_period.end_day)
                        if created:
                            nt.save()
                        Nomination.objects.get_or_create(award_template_id= template.id,group=period.group,nomination_timing=nt)
                else:
                    for nom in group_nominations:
                        print("Iterating the noms");
                        next_nomination_starts_at = add_months(submission_period.start_day,frequencies[frequency]) 
                        next_nomination_ends_at = add_months(submission_period.end_day,frequencies[frequency])
                        next_review_starts_at = add_months(review_period.start_day, frequencies[frequency])
                        next_review_ends_at = add_months(review_period.end_day, frequencies[frequency])
                        next_approval_starts_at = add_months(approval_period.start_day, frequencies[frequency])
                        next_approval_ends_at  = add_months(approval_period.end_day, frequencies[frequency])
                        if next_nomination_starts_at == (datetime.now() + timedelta(hours=24)).date():
                            nt,created = NominationTiming.objects.get_or_create(award_template_id= template.id,start_day=next_nomination_starts_at, end_day=next_nomination_ends_at,
                            review_start_day=next_review_starts_at, review_end_day=next_review_ends_at,
                            approval_start_day=next_approval_starts_at, approval_end_day=next_approval_ends_at)
                            if created:
                                nt.save()
                            nomination = Nomination.objects.get_or_create(award_template_id=template.id,group=period.group,nomination_timing=nt)



@periodic_task(
  run_every=(crontab(minute='*/1')),
  name="email_task",
  ignore_result=True
)
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
    to_admin = list(User.objects.filter(groups__name='Admin'))
    to_manager = list(User.objects.filter(groups__name='Manager'))
    to_tech_jury = list(User.objects.filter(groups__name='Technical Jury Member'))
    to_director = list(User.objects.filter(groups__name='Directorial Board Member'))
    # nominations_admin = Nomination.objects.filter(group__name='Admin')
    submission_start_nominations = Nomination.objects.filter(nomination_timing__start_day=(datetime.today()+ timedelta(hours=24)).date())
    rating_start_nominations = Nomination.objects.filter(nomination_timing__review_start_day=(datetime.today()+ timedelta(hours=24)).date())
    approval_start_nominations = Nomination.objects.filter(nomination_timing__approval_start_day=datetime.today().date())

    submission_end_nominations = Nomination.objects.filter(nomination_timing__end_day=(datetime.today()+ timedelta(hours=24)).date())
    rating_end_nominations = Nomination.objects.filter(nomination_timing__review_end_day=(datetime.today()+ timedelta(hours=24)).date())
    approval_end_nominations = Nomination.objects.filter(nomination_timing__approval_end_day=(datetime.today()+ timedelta(hours=24)).date())


# submissions
    if submission_start_nominations:
        print("Nomination started")
        timing_set = set()
        for nomination in submission_start_nominations:
            timing_set.add(nomination.nomination_timing)
        
        for timing in timing_set:
            submission_recipients = []
            template = timing.award_template
            if template.questions.filter(groups__id=2).exists():
                submission_recipients.extend(list(to_manager))

            if template.questions.filter(groups__id=3).exists():
                submission_recipients.extend(list(to_tech_jury))

            if template.questions.filter(groups__id=4).exists():
                submission_recipients.extend(list(to_director))

            print("Submission start reminder sending...")
            sending(submission_recipients, timing.start_day, timing.end_day, template, 'nominate_app/emails/managers_start-date.html', \
                manager_start_date, str(os.environ['SERVER_NAME'] + reverse('nominate_app:nominations')))



    if submission_end_nominations:
        timing_set = set()
        for nomination in submission_start_nominations:
            timing_set.add(nomination.nomination_timing)
        
        for timing in timing_set:
            submission_recipients = []
            template = timing.award_template
            if template.questions.filter(groups__id=2).exists():
                submission_recipients.extend(list(to_manager))

            if template.questions.filter(groups__id=3).exists():
                submission_recipients.extend(list(to_tech_jury))

            if template.questions.filter(groups__id=4).exists():
                submission_recipients.extend(list(to_director))

            sending(submission_recipients, timing.start_day, timing.end_day, template, 'nominate_app/emails/managers_end-date.html', \
                manager_start_date, str(os.environ['SERVER_NAME'] + reverse('nominate_app:nominations')))


# ratings
    if rating_start_nominations:
        print("Rating started")
        rating_recipients = list(to_tech_jury)
        timing_set = set()
        for nomination in rating_start_nominations:
            timing_set.add(nomination.nomination_timing)

        for timing in timing_set:
            template = timing.award_template
            print("Rating start reminder sending...")
            sending(rating_recipients, timing.review_start_day, timing.review_end_day, template, 'nominate_app/emails/tech_jurys_start-date.html', \
                tech_jury_start_date, str(os.environ['SERVER_NAME'] + reverse('nominate_app:nomination_review_index')))


    if rating_end_nominations:
        rating_recipients = list(to_tech_jury)
        timing_set = set()
        for nomination in rating_end_nominations:
            timing_set.add(nomination.nomination_timing)

        for timing in timing_set:
            template = timing.award_template
            sending(rating_recipients, timing.review_start_day, timing.review_end_day, template, 'nominate_app/emails/tech_jurys_end-date.html', \
                tech_jury_start_date, str(os.environ['SERVER_NAME'] + reverse('nominate_app:nomination_review_index')))


# approvals
    if approval_start_nominations:
        approval_recipients = list(to_director)
        timing_set = set()
        for nomination in approval_start_nominations:
            timing_set.add(nomination.nomination_timing)

        for timing in timing_set:
            template = timing.award_template
            sending(approval_recipients, timing.approval_start_day, timing.approval_end_day, template, 'nominate_app/emails/directors_start-date.html', \
                director_start_date, str(os.environ['SERVER_NAME'] + reverse('nominate_app:approval')))


    if approval_end_nominations:
        approval_recipients = list(to_director)
        timing_set = set()
        for nomination in approval_end_nominations:
            timing_set.add(nomination.nomination_timing)

        for timing in timing_set:
            template = timing.award_template
            sending(approval_recipients, timing.approval_start_day, timing.approval_end_day, template, 'nominate_app/emails/directors_end-date.html', \
                director_start_date, str(os.environ['SERVER_NAME'] + reverse('nominate_app:approval')))

