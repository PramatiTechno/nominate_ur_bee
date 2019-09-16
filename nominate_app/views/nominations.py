from django.shortcuts import render, redirect
from nominate_app.models import NominationPeriod, Awards
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponse, JsonResponse
from nominate_app.forms import AwardsForm, AwardsActiveForm, NominationPeriodForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.template.defaulttags import register
from nominate_app.utils import group_required
from nominate_app.models import Nomination,NominationPeriod, AwardTemplate, NominationInstance, User, Questions, NominationAnswers, NominationSubmitted
from IPython import embed
from datetime import datetime, timedelta

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def change_date(request, nomination_id):
    nomination = Nomination.objects.get(id=nomination_id)
    nt = nomination.nomination_timing
    date = request.POST['date']
    period = request.POST['period']
    if period == 'submission':
        nt.end_day = datetime.strptime(date, '%m/%d/%Y').date()
    if period == 'review':
        nt.review_end_day = datetime.strptime(date, '%m/%d/%Y').date()
    if period == 'approval':
        nt.approval_end_day = datetime.strptime(date, '%m/%d/%Y').date()

    nt.save()
    return JsonResponse({
        'status':'success'
    })

@group_required('Directorial Board Member', 'Technical Jury Member', 'Manager', raise_exception=True)
def index(request):
    requested_user_group = request.user.groups.first()
    nominations = Nomination.objects.filter(group=requested_user_group,nomination_timing__start_day__lte=datetime.today() + timedelta(days=1), nomination_timing__end_day__lte= datetime.today())
    new_nominations = []
    for nomination in nominations:
        nomination_instance = nomination.nominationinstance_set.filter(user=request.user)
        has_question = nomination.award_template.questions_set.filter(groups=requested_user_group).exists() if nomination.award_template else False
        if nomination_instance.count() == 0 and has_question:
            new_nominations.append(nomination)   

    statuses = ['New', 'Saved']

    if requested_user_group.name.lower() == "directorial board member":
        statuses.append('Submitted')
    else:
        statuses.extend(status[0] for status in NominationSubmitted.statuses) 

    page = request.GET.get('page', 1)
    paginator = Paginator(new_nominations, 9)
    try:
        nominations = paginator.page(page)
    except PageNotAnInteger:
        nominations = paginator.page(1)
    except EmptyPage:
        nominations = paginator.page(paginator.num_pages)
    return render(request, 'nominate_app/nominations/index.html', {'data': nominations, 'statuses': statuses, 'selected_status': "new" })
  

@group_required('Directorial Board Member', 'Technical Jury Member', 'Manager', raise_exception=True)
def status_index(request, status_value):
    group = request.user.groups.first()
    statuses = ['New', 'Saved']
    nomination_data = []
    status_code = {
        'submitted': 0,
        'reviewed': 1,
        'approved': 2,
        'dismissed': 3,
        'on hold': 4,
    }

    if group.name.lower() == "directorial board member":
        statuses.append('Submitted')
    else:
        statuses.extend(status[0] for status in NominationSubmitted.statuses) 

    if status_value.lower() == "new":
        return redirect('nominate_app:nominations')


    elif status_value.lower() == "saved":
        nominations = Nomination.objects.filter(group__in=request.user.groups.all(), nomination_timing__start_day__lte= datetime.today(), nomination_timing__end_day__lte= datetime.today())
        for nomination in nominations:
            nomination_instance = nomination.nominationinstance_set.filter(user=request.user)
            if nomination_instance and nomination_instance[0].status == 1:
                nomination.nomination_instance_id = nomination_instance[0].id
                nomination_data.append(nomination)

    elif status_value.lower() in status_code.keys():
        nomination_data = NominationSubmitted.objects.filter(status=status_code[status_value.lower()], email=request.user.email)

    page = request.GET.get('page', 1)
    paginator = Paginator(nomination_data, 9)
    try:
        nominations = paginator.page(page)
    except PageNotAnInteger:
        nominations = paginator.page(1)
    except EmptyPage:
        nominations = paginator.page(paginator.num_pages)
  
    return render(request, 'nominate_app/nominations/index.html', {'data': nominations, 'statuses': statuses, 'selected_status': status_value.lower() })