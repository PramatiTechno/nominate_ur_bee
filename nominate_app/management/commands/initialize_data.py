from nominate_app.models import User, Group, Awards, AwardTemplate, NominationRating,NominationTiming, DirectorComments, NominationPeriod, Nomination, NominationSubmitted, QuestionAnswers, Questions, NominationInstance, NominationAnswers
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
import os

# To run this file use "python manage.py initialize_data"
# This file will populate awards, award_templates, nominations, nomination_instances, questions, nomination_submitted, question_answers, auth_user and auth_user_group.



def create_award(name, frequency, manager_offsets=(0, 0), tech_offsets=(0, 0), director_offsets=(0, 0)):
    m_offset1, m_offset2 = manager_offsets
    t_offset1, t_offset2 = tech_offsets
    d_offset1, d_offset2 = director_offsets
    award1, created = Awards.objects.get_or_create(name=name, frequency=frequency)
    award1.save()
    start_day = datetime.now().date() + timedelta(days=m_offset1)
    end_day = datetime.now().date() + timedelta(days=m_offset2)
    nomination_period1, created = NominationPeriod.objects.get_or_create(start_day=start_day, end_day=end_day, award_id=award1.id, group=groups[1])
    nomination_period1.save()
    start_day = datetime.now().date() + timedelta(days=t_offset1)
    end_day = datetime.now().date() + timedelta(days=t_offset2)
    nomination_period2, created = NominationPeriod.objects.get_or_create(start_day=start_day, end_day=end_day, award_id=award1.id, group=groups[2])
    nomination_period2.save()
    start_day = datetime.now().date() + timedelta(days=d_offset1)
    end_day = datetime.now().date() + timedelta(days=d_offset2)
    nomination_period3, created = NominationPeriod.objects.get_or_create(start_day=start_day, end_day=end_day, award_id=award1.id, group=groups[3])
    nomination_period3.save()
    return award1

def create_question(name, qtype, award_template_id, group_id, options=[], attachment_need=False):
    group = Group.objects.get(id=group_id)
    if attachment_need:
        if qtype == 'subjective':
            question, created = Questions.objects.get_or_create(qname=name, qtype=qtype, award_template_id=award_template_id, \
                attachment_need=attachment_need)
            question.groups.add(group)
        else:
            question, created = Questions.objects.get_or_create(qname=name, qtype=qtype, award_template_id=award_template_id, \
                options=options, attachment_need=attachment_need)
            question.groups.add(group)
    else:
        if qtype == 'subjective':
            question, created = Questions.objects.get_or_create(qname=name, qtype=qtype, award_template_id=award_template_id)
            question.groups.add(group)
        else:
            question, created = Questions.objects.get_or_create(qname=name, qtype=qtype, award_template_id=award_template_id, \
                options=options)
            question.groups.add(group)
        
    question.save()
    return question

def create_questions(at):
    create_question('Name of the person and image', 'SUBJECTIVE', at.id, group_id=groups[1].id, attachment_need=True)
    create_question('Manager Question2', 'OBJECTIVE', at.id, group_id=groups[1].id, options=["Option1", "Option2"])
    create_question('Manager Question3', 'MULTIPLE-CHOICE', at.id, group_id=groups[1].id,\
                    options=["Choice1", "Choice2", "Choice3"])
    
    create_question('Name of the person and image', 'SUBJECTIVE', at.id, group_id=groups[2].id, attachment_need=True)
    create_question('Jury Question2', 'OBJECTIVE', at.id, group_id=groups[2].id, options=["Option1", "Option2"])
    create_question('Jury Question3', 'MULTIPLE-CHOICE', at.id, group_id=groups[2].id,\
                    options=["Choice1", "Choice2", "Choice3"])
    
    create_question('Name of the person and image', 'SUBJECTIVE', at.id, group_id=groups[3].id, attachment_need=True)
    create_question('Director Question2', 'OBJECTIVE', at.id, group_id=groups[3].id, options=["Option1", "Option2"])
    create_question('Director Question3', 'MULTIPLE-CHOICE', at.id, group_id=groups[3].id,\
                    options=["Choice1", "Choice2", "Choice3"])
    
def create_award_template(name, award_id):
    award_template, created = AwardTemplate.objects.get_or_create(template_name=name, award_id=award_id)
    award_template.save()
    return award_template


groups = Group.objects.all()


class Command(BaseCommand):
    help = 'Run to Initialize database'
    def _initialize_data(self):

        admin_user, created = User.objects.get_or_create(username='aneesh.narayanan@imaginea.com', email='aneesh.narayanan@imaginea.com')
        technical_jury_user, created = User.objects.get_or_create(username='sandeep.singh@imaginea.com', email='sandeep.singh@imaginea.com')
        director_user, created = User.objects.get_or_create(username='akhilesh.sharma@imaginea.com', email='akhilesh.sharma@imaginea.com')
        if os.environ['ENVIRONMENT'] == 'DEVELOPMENT' or os.environ['ENVIRONMENT'] == '':
            manager_user, created = User.objects.get_or_create(username='anija.thomas@imaginea.com', email='anija.thomas@imaginea.com')
        elif os.environ['ENVIRONMENT'] == 'STAGING':
            manager_user, created = User.objects.get_or_create(username='muthukrishnan.kasiraman@imaginea.com', email='muthukrishnan.kasiraman@imaginea.com')

        # Save the users.
        admin_user.save()
        manager_user.save()
        director_user.save()
        technical_jury_user.save()

        groups = Group.objects.all()

        # Add Group to the Users.
        admin_user.groups.add(groups[0])
        manager_user.groups.add(groups[1])
        technical_jury_user.groups.add(groups[2])
        director_user.groups.add(groups[3])

        # # Create Awards
        award1 = create_award('WaveRiders', 'QUATERLY', manager_offsets=(1, 5), tech_offsets=(1,5), director_offsets=(1,5))
        award2 = create_award('Infinity', 'QUATERLY', manager_offsets=(0, 5), tech_offsets=(1,5), director_offsets=(2,5))


        # # Create Award Templates
        at11 = create_award_template('Template 1', award1.id)
        at12 = create_award_template('Template 2', award1.id)
        at13 = create_award_template('Template 3', award1.id)
        at21 = create_award_template('Template 1 award2', award2.id)
        at22 = create_award_template('Template 2 award2', award2.id)
        at23 = create_award_template('Template 3 award2', award2.id)
        at24 = create_award_template('Template 4 award2', award2.id)
        at25 = create_award_template('Template 5 award2', award2.id)

        # # Create questions for templates.
        create_questions(at11)
        create_questions(at12)
        create_questions(at13)
        create_questions(at21)
        create_questions(at22)
        create_questions(at23)
        create_questions(at24)
        create_questions(at25)

        # Create Nomination for award2
        manager_nominations = []
        jury_nominations = []
        director_nominations = []
        for at in [at21, at22, at23, at24, at25]:
            periods = at.award.nominationperiod_set.all()
            submission_period = periods.get(group_id=2)
            review_period = periods.get(group_id=3)
            approval_period = periods.get(group_id=4)
            for i in range(1, 4):
                np = NominationPeriod.objects.get(award_id=award2.id,group=groups[i])
                nt,created = NominationTiming.objects.get_or_create(award_template_id= at.id,start_day=submission_period.start_day,end_day=submission_period.end_day,
                            review_start_day=review_period.start_day, review_end_day=review_period.end_day,
                                approval_start_day=approval_period.start_day, approval_end_day=approval_period.end_day)
                if created: 
                    nt.save()
                nomination,nom_created = Nomination.objects.get_or_create(award_template=at, group=groups[i],nomination_timing=nt)
                if nom_created:
                    nomination.save()

                if i == 1:
                    manager_nominations.append(nomination) 
                if i == 2:
                    jury_nominations.append(nomination) 
                if i == 3:
                    director_nominations.append(nomination) 


        save_nominations = []
        submit_nominations = []
 
        save_nominations = manager_nominations[1:3] + jury_nominations[1:3] + director_nominations[1:3]
        submit_nominations = manager_nominations[3:5] + jury_nominations[3:5] + director_nominations[3:5]


        # Create a saved nomination for each user.
        for i in range(0, len(save_nominations)):
            nomination = save_nominations[i]
            if nomination.group == groups[1]:
                user = manager_user
            elif nomination.group == groups[2]:
                user = technical_jury_user
            else:
                user = director_user

            nomination_instance, created = NominationInstance.objects.get_or_create(nomination=nomination, user=user)
            nomination_instance.status = 1
            nomination_instance.save()
            questions = Questions.objects.filter(award_template = nomination.award_template, groups=nomination.group).order_by('id')
            answer1, created = NominationAnswers.objects.get_or_create(answer_option=False, answer_text="TestUser",nomination_instance_id=nomination_instance.id, uploaded_at=timezone.now(), award_template_id=nomination.award_template_id, question_id=questions[0].id, submitted_by=user)
            answer2, created = NominationAnswers.objects.get_or_create(answer_option=True, answer_text=json.dumps(['Option1']),nomination_instance_id=nomination_instance.id, uploaded_at=timezone.now(), award_template_id=nomination.award_template_id, question_id=questions[1].id, submitted_by=user)
            answer3, created = NominationAnswers.objects.get_or_create(answer_option=True, answer_text=json.dumps(["Choice1", "Choice2"]),nomination_instance_id=nomination_instance.id, uploaded_at=timezone.now(), award_template_id=nomination.award_template_id, question_id=questions[2].id, submitted_by=user)
            answer1.save()
            answer2.save()
            answer3.save()
            
        # Create a three nominations for each user, .
        for i in range(0, len(submit_nominations)):
            nomination = submit_nominations[i]
            if nomination.group == groups[1]:
                user = manager_user
            elif nomination.group == groups[2]:
                user = technical_jury_user
            else:
                user = director_user
                
            nomination_instance, created = NominationInstance.objects.get_or_create(nomination=nomination, user=user)
            nomination_instance.status = 2
            nomination_instance.save()
            questions = Questions.objects.filter(award_template = nomination.award_template, groups=nomination.group).order_by('id')
            answer1, created = NominationAnswers.objects.get_or_create(answer_option=False, answer_text="TestUser",nomination_instance_id=nomination_instance.id, uploaded_at=timezone.now(), award_template_id=nomination.award_template_id, question_id=questions[0].id, submitted_by=user)
            answer2, created = NominationAnswers.objects.get_or_create(answer_option=True, answer_text=json.dumps(['Option1']),nomination_instance_id=nomination_instance.id, uploaded_at=timezone.now(), award_template_id=nomination.award_template_id, question_id=questions[1].id, submitted_by=user)
            answer3, created = NominationAnswers.objects.get_or_create(answer_option=True, answer_text=json.dumps(["Choice1", "Choice2"]),nomination_instance_id=nomination_instance.id, uploaded_at=timezone.now(), award_template_id=nomination.award_template_id, question_id=questions[2].id, submitted_by=user)
            answer1.save()
            answer2.save()
            answer3.save()
            nomination_submitted, created = NominationSubmitted.objects.get_or_create(nomination=nomination, status=0, submitted_at=timezone.now(), email=user.email,\
                                                    firstname='test', group=nomination.group, designation='test', lastname='test',\
                                                    award_name=award2.name, worklocation='test', baselocation='test', template_name=nomination.award_template.template_name)
            nomination_submitted.save()
            qa, created = QuestionAnswers.objects.get_or_create(nomination_submitted=nomination_submitted, question=questions[0].qname, answer=answer1.answer_text)
            qa1, created = QuestionAnswers.objects.get_or_create(nomination_submitted=nomination_submitted, question=questions[1].qname, answer=", ".join(json.loads(answer2.answer_text)))
            qa2, created = QuestionAnswers.objects.get_or_create(nomination_submitted=nomination_submitted, question=questions[2].qname, answer=", ".join(json.loads(answer3.answer_text)))
            qa.save()
            qa1.save()
            qa2.save()
        
        submitted_nominations = list(NominationSubmitted.objects.filter(group__name="Manager")[:1]) + \
                                list(NominationSubmitted.objects.filter(group=groups[2])[:1]) + \
                                list(NominationSubmitted.objects.filter(group=groups[3])[:1])
    

        # Create 2 nomination reviews.
        for nomination in submitted_nominations:
            review_user = User.objects.filter(groups__name='Technical Jury Member')[0]
            obj, created = NominationRating.objects.get_or_create(rating="3", review="Great Idea!", submission=nomination, user_id=review_user.id)
            obj.save()
            nomination.status = 1
            nomination.save()    

        # # approve one review.
        approve_nomination = submitted_nominations[0]
        approve_user = User.objects.filter(groups__name='Directorial Board Member')[0]
        obj, created = DirectorComments.objects.get_or_create(comment='Approved !!', nomination_submitted=approve_nomination, user=approve_user)
        obj.save()
        approve_nomination.status = 2
        approve_nomination.save()
    
    def handle(self, *args, **options):
        self._initialize_data()


