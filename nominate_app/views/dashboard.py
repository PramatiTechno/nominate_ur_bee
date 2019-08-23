from nominate_app.models import Nomination,Awards, NominationPeriod, AwardTemplate, NominationInstance, User, Questions, NominationAnswers, NominationSubmitted, NominationRating, DirectorComments, Group
from django.shortcuts import render, redirect
from nominate_app.utils import group_required
from django.template.defaulttags import register


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
    for award in awards_list:
        awards['data'].append(award_status(award.id)['submitted'])    
    if Awards.objects.count() > 5:
        awards['show'] = True 
    recent_nominations = get_recent_nominations()
    notifications = get_notifications()
    summary = {'awards': Awards.objects.count()}
    summary['approved'] = NominationSubmitted.objects.filter(status=2).count()
    summary['declined'] = NominationSubmitted.objects.filter(status=3).count()
    summary['hold'] = NominationSubmitted.objects.filter(status=4).count()
    results = {'awards': awards, 'recent_nominations': recent_nominations, 'notifications': notifications, 'summary': summary}
    results.update(graph_data)
    return render(request, 'nominate_app/dashboard.html', results)

def get_notifications():
    return NominationSubmitted.objects.all().order_by('updated_at').reverse()[:3]


def get_recent_nominations():
    nominations = Nomination.objects.all().order_by('end_day')[:3]
    return nominations
def award_status(award_id):
    award = Awards.objects.get(id=award_id)
    awards = Awards.objects.all()
    groups = Group.objects.all()
    group_names = [group.name.lower() for group in groups]
    
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
    return result


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