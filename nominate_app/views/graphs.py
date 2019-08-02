from django.shortcuts import render, redirect
from nominate_app.models import NominationPeriod, Awards, Group
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponse
from nominate_app.forms import AwardsForm, AwardsActiveForm, NominationPeriodForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from nominate_app.utils import group_required
from datetime import datetime
from IPython import embed

@group_required('Admin', raise_exception=True)
def index(request):
    awards = Awards.objects.all()
    return render(request, 'nominate_app/graphs.html', {"award_categories": awards})

@group_required('Admin', raise_exception=True)
def load_graph(request, award_id):
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
    return render(request, 'nominate_app/graphs.html', {"award_categories": awards, "award_stats": result, "award_selected": award})