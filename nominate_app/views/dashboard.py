from nominate_app.models import Nomination,Awards, NominationPeriod, AwardTemplate, NominationInstance, User, Questions, NominationAnswers, NominationSubmitted, NominationRating, DirectorComments, Group
from django.shortcuts import render, redirect
from nominate_app.utils import group_required
from django.template.defaulttags import register
from datetime import datetime,timedelta
from django.db.models import Q
from django.db.models import Count
from IPython import embed


@register.filter
def get(dict, key):
    return dict[key]

@register.filter
def get_status(submission, status_code):
    return submission.get_status(status_code).lower()

def index(request):
    
    award = request.GET.get('award',default=None)
    graph_data = load_graph(award)
    awards_list = Awards.objects.all().order_by('created_at').reverse()[:4]
    
    awards = {'data': [], 'show': False}
    
    recent_nominations = get_recent_nominations()
    notifications = get_notifications()
    activities = get_activities(request.user)
    summary = {'awards': Awards.objects.count()}
    summary['approved'] = NominationSubmitted.objects.filter(status=2).count()
    summary['declined'] = NominationSubmitted.objects.filter(status=3).count()
    summary['hold'] = NominationSubmitted.objects.filter(status=4).count()
    results = {'awards': awards, 'recent_nominations': recent_nominations, 'notifications': notifications, 'summary': summary}
    results.update(graph_data)
    for award in awards_list:
        awards['data'].append(results['award_stats']['submitted'])    
    if Awards.objects.count() > 3:
        awards['show'] = True
    results.update(activities)
    return render(request, 'nominate_app/dashboard.html', results)

def get_notifications():
    notifications = list()
    submissions = NominationSubmitted.objects.all().order_by('-updated_at')[:3]
    for submission in submissions:
        data = dict()
        data['user'] = submission.get_user(submission.status)
        data['status'] = submission.get_status(submission.status).lower()
        data['award'] = submission.award_name
        notifications.append(data)
    return notifications


def get_recent_nominations():
    nominations = Nomination.objects.all().order_by('end_day')[:3]
    return nominations

def get_activities(user_obj):
    unsubmitted_list = []
    submissions = NominationSubmitted.objects.filter(email=user_obj.email, \
        nomination__end_day__gte=datetime.now().date())
    for sub in submissions: 
        template_date = dict() 
        template_date['template_name']=sub.nomination.award_template.template_name
        template_date['time']=sub.nomination.end_day.strftime('%B %d')
        template_date['status']=sub.get_status(sub.status) 
        unsubmitted_list.append(template_date) 
    submitted_list = []
    for nom in NominationSubmitted.objects.filter(Q(submitted_at__gte=(datetime.now()- timedelta(weeks=1)).date()) |Q(updated_at__gte=(datetime.now()-timedelta(weeks=1)).date()),email=user_obj.email):
        submitted_date = dict()
        submitted_date['status']=nom.get_status(nom.status)
        submitted_date['template_name']=nom.nomination.award_template.template_name 
        submitted_date['reviewed_by'] = nom.get_user(nom.status)
        submitted_date['time']=nom.submitted_at.strftime('%B %d')
        submitted_list.append(submitted_date)
    my_like_list = get_likes(user_obj)
    my_comments_list = get_comments(user_obj)
    my_graph = get_mygraph(user_obj)
    published_results = get_published_results()
    return {'likes_list':my_like_list, 'comment_list':my_comments_list, \
        'template_date':unsubmitted_list, 'submitted_date':submitted_list, \
            'graph_data':my_graph, 'published_results':published_results}

def get_likes(user):
    my_like_list = []
    for instance in user.nominationinstance_set.all():
        for submissions in instance.nomination.submissions.\
            filter(Q(created_at__gte=(datetime.now()- timedelta(weeks=1)).date()) |\
                 Q(updated_at__gte=(datetime.now()-timedelta(weeks=1)).date())):
            for like in submissions.likes.all():
                z = dict()
                z[instance.nomination.award_template.template_name]=\
                    str(like.voter.first_name) + " " + str(like.voter.last_name)
                my_like_list.append(z)
    return my_like_list

def get_comments(user):
    my_comments_list = []
    for instance in user.nominationinstance_set.all():
        for submissions in instance.nomination.submissions.\
            filter(Q(created_at__gte=(datetime.now()- timedelta(weeks=1)).date()) |\
                 Q(updated_at__gte=(datetime.now()-timedelta(weeks=1)).date())):
            for comment in submissions.comments.all():
                z = dict()
                z[instance.nomination.award_template.template_name]=\
                    str(comment.author.first_name) + " " + str(comment.author.last_name)
                my_comments_list.append(z)
    return my_comments_list

def get_mygraph(user):
    submissions = NominationSubmitted.objects.filter(email=user.email)
    data = dict()
    data['Submitted'] = submissions.filter(status=0).count()
    data['Reviewed'] = submissions.filter(status=1).count()
    data['Approved'] = submissions.filter(status=2, is_published=True).count()
    data['Dismissed'] = submissions.filter(status=3,is_published=True).count()
    data['On hold'] = submissions.filter(status=4,is_published=True).count()
    return  data

def get_published_results():
    published = NominationSubmitted.objects.\
        filter(Q(created_at__gte=(datetime.now()- timedelta(weeks=1)).date()) |\
                 Q(updated_at__gte=(datetime.now()-timedelta(weeks=1)).date()))\
                     .order_by('-updated_at')
    results = list()
    for result in published:
        results.append(result.nomination.award_template.template_name)
    return results

def load_graph(award_id):
    if award_id:
        award = Awards.objects.get(id=award_id)
    elif Awards.objects.count() > 0:
        award = Awards.objects.first()
    else:
        award = None
    if award:
        result = {
        "submitted": {
            "award_name": award.name,
            "status": "submitted",
            "data": {
            }
        },
        "saved": {
            "award_name": award.name,
            "status": "saved",
            "data": {
            }
        }
        }

        awards = Awards.objects.all()
        groups = Group.objects.all()
        group_names = [group.name.lower() for group in groups]
        
        
        for group_name in group_names:
            result['submitted']['data'].update({ group_name: 0 })
            result['saved']['data'].update({ group_name: 0 })
        for award_template in award.awardtemplate_set.all():
            for nomination in award_template.nomination_set.all():
                for nomination_instance in nomination.nominationinstance_set.all():
                    if nomination_instance.get_status(nomination_instance.status).lower() == "submitted":
                        
                        group_name = nomination_instance.user.groups.first().name.lower()
                        result['submitted']['data'][group_name] += 1
                    elif nomination_instance.get_status(nomination_instance.status).lower() == "saved":
                        group_name = nomination_instance.user.groups.first().name.lower()
                        result['saved']['data'][group_name] += 1
        result['submitted']['data'].pop("admin")
        result['saved']['data'].pop("admin")
    else:
        awards = None
        result = {
            'submitted':{
                'data':{

                }
            },'saved':{
                'data':{

                }
            }
        }
        groups = Group.objects.all()
        
        group_names = [group.name.lower() for group in groups]
    

        for group_name in group_names:
            result['submitted']['data'].update({ group_name: 0 })
            result['saved']['data'].update({ group_name: 0 })
        result['submitted']['data'].pop("admin")
        result['saved']['data'].pop("admin")
    return {"award_categories": awards, "award_stats": result, "award_selected": award}