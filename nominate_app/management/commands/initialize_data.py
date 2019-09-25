from nominate_app.models import User, Group, Awards, AwardTemplate, NominationRating, \
    NominationTiming, DirectorComments, NominationPeriod, Nomination, NominationSubmitted, \
        QuestionAnswers, Questions, NominationInstance, NominationAnswers, UserProfile
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
        groups = Group.objects.all()
        if os.environ['ENVIRONMENT'] == 'DEVELOPMENT' or os.environ['ENVIRONMENT'] == '':
            admin_user, created = User.objects.get_or_create(username='aneesh.narayanan@imaginea.com', email='aneesh.narayanan@imaginea.com')
            technical_jury_user, created = User.objects.get_or_create(username='sandeep.singh@imaginea.com', email='sandeep.singh@imaginea.com')
            director_user, created = User.objects.get_or_create(username='akhilesh.sharma@imaginea.com', email='akhilesh.sharma@imaginea.com')
            manager_user, created = User.objects.get_or_create(username='anija.thomas@imaginea.com', email='anija.thomas@imaginea.com')
            admin_user.groups.add(groups[0])
            manager_user.groups.add(groups[1])
            technical_jury_user.groups.add(groups[2])
            director_user.groups.add(groups[3])
        elif os.environ['ENVIRONMENT'] == 'STAGING':
            user_data = {
                0:{'muthukrishnan.kasiraman@imaginea.com':{
                                                'designation':'HR', 
                                                'telephonenumber':'9123456780', 
                                                'employeenumber':'13101', 
                                                'jobtitle':'HR', 
                                                'cn':'India', 
                                                'title':'HR', 
                                                'lastpwdchange':'Pramati123', 
                                                'defaultpwd':'Pramati', 
                                                'baselocation':'WS-A220', 
                                                'uid':'13101', 
                                                'worklocation':'Chennai'
                                                },
                    'aneesh.narayanan@imaginea.com':{
                                                'designation':'HR', 
                                                'telephonenumber':'9123456780', 
                                                'employeenumber':'13111', 
                                                'jobtitle':'HR', 
                                                'cn':'India', 
                                                'title':'HR', 
                                                'lastpwdchange':'Pramati123', 
                                                'defaultpwd':'Pramati', 
                                                'baselocation':'WS-A920', 
                                                'uid':'13111', 
                                                'worklocation':'Chennai'
                                                    },
                    'sandeep.singh@imaginea.com':{
                                                'designation':'HR', 
                                                'telephonenumber':'9123456781', 
                                                'employeenumber':'13102', 
                                                'jobtitle':'HR', 
                                                'cn':'India', 
                                                'title':'HR', 
                                                'lastpwdchange':'Pramati123', 
                                                'defaultpwd':'Pramati', 
                                                'baselocation':'WS-A221', 
                                                'uid':'13102', 
                                                'worklocation':'Chennai'                        
                                                }, 
                    'akhilesh.sharma@imaginea.com':{
                                                'designation':'HR', 
                                                'telephonenumber':'9123456782', 
                                                'employeenumber':'13103', 
                                                'jobtitle':'HR', 
                                                'cn':'India', 
                                                'title':'HR', 
                                                'lastpwdchange':'Pramati123', 
                                                'defaultpwd':'Pramati', 
                                                'baselocation':'WS-A222', 
                                                'uid':'13103', 
                                                'worklocation':'Chennai'
                                                    }
                    }, 
                1:{'ramya.raju@imaginea.com':{
                                                'designation':'Manager', 
                                                'telephonenumber':'9123456783', 
                                                'employeenumber':'13104', 
                                                'jobtitle':'Manager', 
                                                'cn':'India', 
                                                'title':'Manager', 
                                                'lastpwdchange':'Pramati123', 
                                                'defaultpwd':'Pramati123', 
                                                'baselocation':'WS-A223', 
                                                'uid':'13104', 
                                                'worklocation':'Chennai'
                                            }, 
                'nishant.das@imaginea.com':{
                                                'designation':'Manager', 
                                                'telephonenumber':'9123456784', 
                                                'employeenumber':'13105', 
                                                'jobtitle':'Manager', 
                                                'cn':'India', 
                                                'title':'Manager', 
                                                'lastpwdchange':'Pramati123', 
                                                'defaultpwd':'Pramati123', 
                                                'baselocation':'WS-A224', 
                                                'uid':'13105', 
                                                'worklocation':'Chennai'
                                            }, 
                'arun.balan@imaginea.com':{
                                                'designation':'Manager', 
                                                'telephonenumber':'9123456785', 
                                                'employeenumber':'13106', 
                                                'jobtitle':'Manager', 
                                                'cn':'India', 
                                                'title':'Manager', 
                                                'lastpwdchange':'Pramati123', 
                                                'defaultpwd':'Pramati123', 
                                                'baselocation':'WS-A225', 
                                                'uid':'13106', 
                                                'worklocation':'Chennai'
                                            }
                }, 
                2:{'nishanthini.ramu@imaginea.com':{
                                                'designation':'Architect', 
                                                'telephonenumber':'9123456786', 
                                                'employeenumber':'13107', 
                                                'jobtitle':'Architect', 
                                                'cn':'India', 
                                                'title':'Development', 
                                                'lastpwdchange':'Pramati123', 
                                                'defaultpwd':'Pramati123', 
                                                'baselocation':'WS-A226', 
                                                'uid':'13107', 
                                                'worklocation':'Chennai'
                                                    }, 
                'kishorekumar.arul@imaginea.com':{
                                                'designation':'Architect', 
                                                'telephonenumber':'9123456787', 
                                                'employeenumber':'13108', 
                                                'jobtitle':'Architect', 
                                                'cn':'India', 
                                                'title':'Development', 
                                                'lastpwdchange':'Pramati123', 
                                                'defaultpwd':'Pramati123', 
                                                'baselocation':'WS-A227', 
                                                'uid':'13108', 
                                                'worklocation':'Chennai'
                                                }, 
                'vignesh.kanagaraj@imaginea.com':{
                                                'designation':'Architect', 
                                                'telephonenumber':'9123456788', 
                                                'employeenumber':'13109', 
                                                'jobtitle':'Architect', 
                                                'cn':'India', 
                                                'title':'QA', 
                                                'lastpwdchange':'Pramati123', 
                                                'defaultpwd':'Pramati123', 
                                                'baselocation':'WS-A228', 
                                                'uid':'13109', 
                                                'worklocation':'Chennai'
                                                }
                }, 
                3:{'saravanan.murugesan@imaginea.com':{
                                                'designation':'Director', 
                                                'telephonenumber':'9123456789', 
                                                'employeenumber':'13110', 
                                                'jobtitle':'Director', 
                                                'cn':'India', 
                                                'title':'Director', 
                                                'lastpwdchange':'Pramati123', 
                                                'defaultpwd':'Pramati123', 
                                                'baselocation':'WS-A229', 
                                                'uid':'13110', 
                                                'worklocation':'Chennai'
                                                    }, 
                'nimmy.vipin@imaginea.com':{
                                                'designation':'Director', 
                                                'telephonenumber':'9123456790', 
                                                'employeenumber':'13111', 
                                                'jobtitle':'Director', 
                                                'cn':'India', 
                                                'title':'Director', 
                                                'lastpwdchange':'Pramati123', 
                                                'defaultpwd':'Pramati123', 
                                                'baselocation':'WS-A230', 
                                                'uid':'13111', 
                                                'worklocation':'Chennai'
                                            }, 
                'anjali.devi@imaginea.com':{
                                                'designation':'Director', 
                                                'telephonenumber':'9123456791', 
                                                'employeenumber':'13112', 
                                                'jobtitle':'Director', 
                                                'cn':'India', 
                                                'title':'Director', 
                                                'lastpwdchange':'Pramati123', 
                                                'defaultpwd':'Pramati123', 
                                                'baselocation':'WS-A231', 
                                                'uid':'13112', 
                                                'worklocation':'Chennai'
                                            }
                }
                }
            for group in user_data.keys():
                for username in user_data[group].keys():
                    # if username not in ['aneesh.narayanan@imaginea.com', 'akhilesh.sharma@imaginea.com', 'sandeep.singh@imaginea.com', 'muthukrishnan.kasiraman@imaginea.com']:
                        user, created = User.objects.get_or_create(username=username, email=username)
                        user.groups.add(groups[group])
                        value = user_data[group][username]
                        # UserProfile.objects.get_or_create(email=user.email, designation=value['designation'], \
                        #     telephonenumber=value['telephonenumber'], employeenumber=value['employeenumber'], \
                        #         jobtitle=value['jobtitle'], cn=value['cn'], title=value['title'], \
                        #             lastpwdchange=value['lastpwdchange'], defaultpwd=value['defaultpwd'], \
                        #                 baselocation=value['baselocation'],uid=value['uid'], \
                        #                     worklocation=value['worklocation'], user_id=user.id)


        # # Create Awards
        awards_data = {
        'Infinity':{'frequency':'MONTHLY', 
                    1:{'start_day':'01/01/19', 'end_day':'01/07/19'},
                    2:{'start_day':'01/08/19', 'end_day':'01/14/19'},
                    3:{'start_day':'01/15/19','end_day':'01/21/19'}},
        'Engage':{'frequency':'QUATERLY',
                    1:{'start_day':'01/01/19', 'end_day':'03/31/19'}, 
                    2:{'start_day':'01/01/19', 'end_day':'03/31/19'}, 
                    3:{'start_day':'01/01/19', 'end_day':'03/31/19'}},
        'Spot':{'frequency':'YEARLY',
                    1:{'start_day':'01/01/19', 'end_day':'12/31/19'}, 
                    2:{'start_day':'01/01/19', 'end_day':'12/31/19'}, 
                    3:{'start_day':'01/01/19', 'end_day':'12/31/19'}},        
        'Gold Class':{'frequency':'MONTHLY',
                    1:{'start_day':'01/01/19', 'end_day':'01/07/19'}, 
                    2:{'start_day':'01/08/19', 'end_day':'01/14/19'}, 
                    3:{'start_day':'01/15/19', 'end_day':'01/21/19'}},        
        'Rave':{'frequency':'QUATERLY',
                    1:{'start_day':'01/01/19', 'end_day':'03/31/19'}, 
                    2:{'start_day':'01/01/19', 'end_day':'03/31/19'}, 
                    3:{'start_day':'01/01/19', 'end_day':'03/31/19'}},        
        'Good Performer':{'frequency':'YEARLY',
                    1:{'start_day':'01/01/19', 'end_day':'12/31/19'}, 
                    2:{'start_day':'01/01/19', 'end_day':'12/31/19'}, 
                    3:{'start_day':'01/01/19', 'end_day':'12/31/19'}},
        'Difference  Maker':{'frequency':'QUATERLY',
                    1:{'start_day':'09/26/19', 'end_day':'09/27/19'}, 
                    2:{'start_day':'09/26/19', 'end_day':'09/27/19'}, 
                    3:{'start_day':'09/26/19', 'end_day':'09/27/19'}},
        'Ultimate team player':{'frequency':'QUATERLY',
                    1:{'start_day':'09/26/19', 'end_day':'09/27/19'}, 
                    2:{'start_day':'09/26/19', 'end_day':'09/27/19'}, 
                    3:{'start_day':'09/26/19', 'end_day':'09/27/19'}},
        }
        template_data = {
            'Infinity':[{'template': 'Infinity Final', 
                        'template_data_1':{'Question':'Provide justifications.','Question Type': 'subjective','group':[1],'Need Attachment':True},
                        'template_data_2':{'Question':'Provide justifications.','Question Type': {'objective':['Beginner', 'Intermediate', 'Expertise', 'Excellent']},'group':[1],'Need Attachment':False},
                        'template_data_3':{'Question':'Provide justifications.','Question Type': {'multiple-choice':['Beginner', 'Intermediate', 'Expertise', 'Excellent']},'group':[2,3],'Need Attachment':True},
                        },
                        {'template':'Infinity Runner Up',
                        'template_data_1':{'Question':'What are the points to consider?', 'Question Type': 'subjective','group':[2,3],'Need Attachment':False},
                        'template_data_2':{'Question':'What are the points to consider?', 'Question Type': {'objective':['Intermediate','Expertise', 'Excellent']},'group':[1, 2, 3],'Need Attachment':True},
                        'template_data_3':{'Question':'What are the points to consider?', 'Question Type': {'multiple-choice':['Intermediate','Expertise','Excellent']},'group':[1],'Need Attachment':False}
                        },
                        {'template':'Infinity Last',
                        'template_data_1':{'Question':'What are the reasons?', 'Question Type': 'subjective','group':[2,3],'Need Attachment':True},
                        'template_data_2':{'Question':'What are the reasons?', 'Question Type': {'objective':['Beginner', 'Intermediate','Expertise', 'Excellent']},'group':[1,2,3],'Need Attachment':False},
                        'template_data_3':{'Question':'What are the reasons?', 'Question Type': {'multiple-choice':['Beginner', 'Intermediate','Expertise', 'Excellent']},'group':[1, 2, 3],'Need Attachment':True}
                        },
                        ],
            'Engage':[{'template':'Engage Final',
                    'template_data_1':{'Question':'Reasons for the nomination.', 'Question Type': 'subjective','group':[1, 2],'Need Attachment':True},
                    'template_data_2':{'Question':'Reasons for the nomination.', 'Question Type': {'objective':['Beginner', 'Intermediate', 'Expertise']},'group':[2],'Need Attachment':False},
                    'template_data_3':{'Question':'Reasons for the nomination.', 'Question Type': {'multiple-choice':['Beginner', 'Intermediate', 'Expertise']},'group':[1, 2, 3],'Need Attachment':False},
                     },
                    {'template':'Engage Runner Up',
                    'template_data_1':{'Question':'Atleast provide one reason for nomination.', 'Question Type': 'subjective','group':[1,2],'Need Attachment':False},
                    'template_data_2':{'Question':'Atleast provide one reason for nomination.', 'Question Type': {'objective':['Expertise', 'Excellent']},'group':[1, 2, 3],'Need Attachment':True},
                    'template_data_3':{'Question':'Atleast provide one reason for nomination.', 'Question Type': {'multiple-choice':['Expertise','Excellent']},'group':[1],'Need Attachment':False}
                    },
                    {'template':'Engage Last',
                    'template_data_1':{'Question':'What are the highlights?', 'Question Type': 'subjective','group':[1,2,3],'Need Attachment':False},
                    'template_data_2':{'Question':'What are the highlights?', 'Question Type': {'objective':['Beginner', 'Intermediate','Expertise']},'group':[3],'Need Attachment':True},
                    'template_data_3':{'Question':'What are the highlights?', 'Question Type': {'multiple-choice':['Beginner', 'Intermediate','Expertise']},'group':[1, 2],'Need Attachment':False}
                     },                    
                     ],
            'Spot':[{'template':'Spot Final',
                    'template_data_1':{'Question':'What are the justifications?', 'Question Type': 'subjective','group':[1, 3],'Need Attachment':True},
                    'template_data_2':{'Question':'What are the justifications?', 'Question Type': {'objective':['Intermediate', 'Expertise', 'Excellent']},'group':[3],'Need Attachment':False}, 
                    'template_data_3':{'Question':'What are the justifications?', 'Question Type': {'multiple-choice':['Intermediate', 'Expertise', 'Excellent']},'group':[1, 2, 3],'Need Attachment':True}
                    },
                    {'template':'Spot Runner Up',
                    'template_data_1':{'Question':'What are the key highlights?', 'Question Type': 'subjective','group':[1,2,3],'Need Attachment':False},
                    'template_data_2':{'Question':'What are the key highlights?', 'Question Type': {'objective':['Beginner', 'Intermediate', 'Expertise', 'Excellent']},'group':[2],'Need Attachment':True},
                    'template_data_3':{'Question':'What are the key highlights?', 'Question Type': {'multiple-choice':['Beginner', 'Intermediate', 'Expertise', 'Excellent']},'group':[1],'Need Attachment':True}
                    },
                    {'template':'Spot Last',
                    'template_data_1':{'Question':'What is the ROI?', 'Question Type': 'subjective','group':[1,2,3],'Need Attachment':True},
                    'template_data_2':{'Question':'What is the ROI?', 'Question Type': {'objective':['Intermediate','Expertise','Excellent']},'group':[1,3],'Need Attachment':False},
                    'template_data_3':{'Question':'What is the ROI?', 'Question Type': {'multiple-choice':['Intermediate','Expertise', 'Excellent']},'group':[1, 2, 3],'Need Attachment':True}
                    }                                        
                    ],
            'Gold Class':[{'template':'Gold Class Final',
                    'template_data_1':{'Question':'What are the reasons?', 'Question Type': 'subjective','group':[1, 2, 3],'Need Attachment':True},
                    'template_data_2':{'Question':'What are the reasons?', 'Question Type': {'objective':['Expertise', 'Excellent']},'group':[1],'Need Attachment':False},
                    'template_data_3':{'Question':'What are the reasons?', 'Question Type': {'multiple-choice':['Expertise', 'Excellent']},'group':[1],'Need Attachment':False}
                    },
                    {'template':'Gold Class Runner Up',
                    'template_data_1':{'Question':'Provide justifications.', 'Question Type': 'subjective','group':[1,2,3],'Need Attachment':False},
                    'template_data_2':{'Question':'Provide justifications.', 'Question Type': {'objective':['Beginner', 'Intermediate', 'Expertise']},'group':[2, 3],'Need Attachment':True},
                    'template_data_3':{'Question':'Provide justifications.', 'Question Type': {'multiple-choice':['Beginner', 'Intermediate', 'Expertise']},'group':[1,2,3],'Need Attachment':False}
                    },
                    {'template':'Gold Class Last',
                    'template_data_1':{'Question':'What are the points to consider?', 'Question Type': 'subjective','group':[1],'Need Attachment':False},
                    'template_data_2':{'Question':'What are the points to consider?', 'Question Type': {'objective':['Expertise','Excellent']},'group':[2,3],'Need Attachment':True},
                    'template_data_3':{'Question':'What are the points to consider?', 'Question Type': {'multiple-choice':['Expertise', 'Excellent']},'group':[1, 2, 3],'Need Attachment':True}
                    },                    
                    ],
            'Rave':[{'template':'Rave Final',
                    'template_data_1':{'Question':'What are the highlights?', 'Question Type': 'subjective','group':[1, 2, 3],'Need Attachment':True},
                    'template_data_2':{'Question':'What are the highlights?', 'Question Type': {'objective':['Beginner','Intermediate','Expertise', 'Excellent']},'group':[1, 2],'Need Attachment':False},
                    'template_data_3':{'Question':'What are the highlights?', 'Question Type': {'multiple-choice':['Beginner', 'Intermediate','Expertise', 'Excellent']},'group':[2],'Need Attachment':True}
                    },
                    {'template':'Rave Runner Up',
                    'template_data_1':{'Question':'Reasons for the nomination.', 'Question Type': 'subjective','group':[3],'Need Attachment':False},
                    'template_data_2':{'Question':'Reasons for the nomination.', 'Question Type': {'objective':['Intermediate', 'Expertise', 'Excellent']},'group':[1,2],'Need Attachment':True},
                    'template_data_3':{'Question':'Reasons for the nomination.', 'Question Type': {'multiple-choice':['Intermediate', 'Expertise', 'Excellent']},'group':[1, 2, 3],'Need Attachment':True}
                    },
                    {'template':'Rave Last',
                    'template_data_1':{'Question':'Atleast provide one reason for nomination.', 'Question Type': 'subjective','group':[2],'Need Attachment':True},
                    'template_data_2':{'Question':'Atleast provide one reason for nomination.', 'Question Type': {'objective':['Beginner','Intermediate','Expertise','Excellent']},'group':[1,2,3],'Need Attachment':False},
                    'template_data_3':{'Question':'Atleast provide one reason for nomination.', 'Question Type': {'multiple-choice':['Beginner','Intermediate','Expertise', 'Excellent']},'group':[3],'Need Attachment':False}
                    },                    
                    ],
            'Good Performer':[{'template':'Good Performer Final',
                    'template_data_1':{'Question':'What is the ROI?', 'Question Type': 'subjective','group':[2],'Need Attachment':True},
                    'template_data_2':{'Question':'What is the ROI?', 'Question Type': {'objective':['Beginner','Intermediate','Expertise']},'group':[1, 3],'Need Attachment':False},
                    'template_data_3':{'Question':'What is the ROI?', 'Question Type': {'multiple-choice':['Beginner', 'Intermediate','Expertise']},'group':[2],'Need Attachment':False}
                    },
                    {'template':'Good Performer Runner Up',
                    'template_data_1':{'Question':'What are the justifications?', 'Question Type': 'subjective','group':[1,3],'Need Attachment':False},
                    'template_data_2':{'Question':'What are the justifications?', 'Question Type': {'objective':['Expertise', 'Excellent']},'group':[1,2,3],'Need Attachment':True},
                    'template_data_3':{'Question':'What are the justifications?', 'Question Type': {'multiple-choice':['Expertise', 'Excellent']},'group':[1, 2, 3],'Need Attachment':False}
                    },
                    {'template':'Good Performer Last',
                    'template_data_1':{'Question':'What are the key highlights?', 'Question Type': 'subjective','group':[3],'Need Attachment':False},
                    'template_data_2':{'Question':'What are the key highlights?', 'Question Type': {'objective':['Beginner','Intermediate','Expertise']},'group':[1,2,3],'Need Attachment':True},
                    'template_data_3':{'Question':'What are the key highlights?', 'Question Type': {'multiple-choice':['Beginner','Intermediate','Expertise']},'group':[3],'Need Attachment':False}
                    }                    
                    ]
        }

        if os.environ['ENVIRONMENT'] == 'DEVELOPMENT' or os.environ['ENVIRONMENT'] == '':
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
        elif os.environ['ENVIRONMENT'] == 'STAGING':
            for data in awards_data.keys():
                award, a_create = Awards.objects.get_or_create(name=data, frequency=awards_data[data]['frequency'])
                print('---------->>>>>',award)
                for period in range(1,4):
                    NominationPeriod.objects.get_or_create(group_id=period, award_id=award.id, \
                        start_day=datetime.strptime(awards_data[data][period]['start_day'], '%m/%d/%y'), \
                            end_day=datetime.strptime(awards_data[data][period]['end_day'], '%m/%d/%y'))
                try:
                    for temp_data in template_data[data]:
                        award_template, at_create = AwardTemplate.objects.get_or_create(template_name=temp_data['template'], award_id=award.id)
                        question_data = list(temp_data.keys())
                        question_data.remove('template')
                        for ques_data in question_data:
                            try:qtype = list(temp_data[ques_data]['Question Type'].keys())[0]
                            except:qtype = temp_data[ques_data]['Question Type']
                            question, q_create = Questions.objects.get_or_create(qname=temp_data[ques_data]['Question'], qtype=qtype, award_template_id=award_template.id, attachment_need=temp_data[ques_data]['Need Attachment'])
                            question.groups.add(*temp_data[ques_data]['group'])
                except:pass
    
    def handle(self, *args, **options):
        self._initialize_data()


