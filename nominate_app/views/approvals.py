from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from nominate_app.utils import group_required
from nominate_app.models import Nomination,NominationPeriod, AwardTemplate, NominationInstance, User, Questions, NominationAnswers, NominationSubmitted

@group_required('Directorial Board Member', raise_exception=True)
def index(request):
    current_user = User.objects.get(id=request.user.id)
    nominations = Nomination.objects.filter(group__in=list(map(lambda x: x['id'],current_user.groups.values()))) #,start_day__gt= datetime.today(),end_day__lt= datetime.today() )#list(map(lambda g: g.id,current_user.groups.all()))) 
    new_nominations = []
    statuses = []
    statuses.extend(status[0] for status in NominationSubmitted.statuses)
    page = request.GET.get('page', 1)
    paginator = Paginator(new_nominations, 9)
    try:
        nominations = paginator.page(page)
    except PageNotAnInteger:
        nominations = paginator.page(1)
    except EmptyPage:
        nominations = paginator.page(paginator.num_pages)
    return render(request, 'nominate_app/approvals/index.html', {'data': nominations, 'statuses': statuses, 'selected_status': "Submitted" })

def status_index(request, status_value):
    current_user = User.objects.get(id=request.user.id)
    nomination_data = []
    statuses = []
    statuses.extend(status[0] for status in NominationSubmitted.statuses)

    if status_value.lower() == "submitted":
        nomination_data = NominationSubmitted.objects.filter(status=0)
    elif status_value.lower() == "reviewed":
        nomination_data = NominationSubmitted.objects.filter(status=1)
    elif status_value.lower() == "approved":
        nomination_data = NominationSubmitted.objects.filter(status=2)
    elif status_value.lower() == "dismissed":
        nomination_data = NominationSubmitted.objects.filter(status=3)
    else:
        nomination_data = NominationSubmitted.objects.filter(status=4)
    page = request.GET.get('page', 1)
    paginator = Paginator(nomination_data, 9)
    try:
        nominations = paginator.page(page)
    except PageNotAnInteger:
        nominations = paginator.page(1)
    except EmptyPage:
        nominations = paginator.page(paginator.num_pages)
    
    return render(request, 'nominate_app/approvals/index.html', {'data': nominations, 'statuses': statuses, 'selected_status': status_value.lower() })