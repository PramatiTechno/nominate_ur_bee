from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg
from django.utils import timezone
from nominate_app.utils import group_required
from nominate_app.models import *
from django.template.defaulttags import register
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from itertools import chain

@register.filter
def get_user(value, arg):
    return User.objects.get(id=arg)

@register.filter
def get_status(submission, status_code):
    return submission.get_status(status_code)

@group_required('Directorial Board Member', raise_exception=True)
def index(request):
    
    selected_status = request.GET.get('status', default='reviewed')
    current_user = User.objects.get(id=request.user.id)
    page = request.GET.get('page', 1)
    today = datetime.today().date()
    statuses = ['reviewed', 'history']
    if selected_status == 'reviewed':
        nomination_data = NominationSubmitted.objects.filter(status=1, nomination__end_day__gte=today)
    elif selected_status == 'history':
        nomination_data = NominationSubmitted.objects.filter(status__in=[2, 3, 4])
    paginator = Paginator(nomination_data, 9)
    try:
        nominations = paginator.page(page)
    except PageNotAnInteger:
        nominations = paginator.page(1)
    except EmptyPage:
        nominations = paginator.page(paginator.num_pages)
    
    return render(request, 'nominate_app/approvals/index.html', {'data': nominations, 'statuses': statuses, 'selected_status': selected_status })

@group_required('Directorial Board Member', raise_exception=True)
def approve(request, submission_id):
    if request.method == "POST":
        dc = DirectorComments(nomination_submitted_id=submission_id, user=request.user, comment=request.POST['comment'])
        dc.save()
        status = request.POST['selected_option']
        nomination_submitted = NominationSubmitted.objects.get(id=submission_id)
        if status.lower() == 'approved':
            nomination_submitted.status = 2
        elif status.lower() == 'dismissed':
            nomination_submitted.status = 3
        else:
            nomination_submitted.status = 4
        nomination_submitted.updated_at = timezone.now()
        nomination_submitted.save()
        # to manager and jury telling results will be declared soon
        subject_all = 'Results coming soon !!!'
        to_manager_and_tech_jury = list(chain(User.objects.filter(groups__name='Manager'), \
            User.objects.filter(groups__name='Technical Jury Member')))
        for recipient in to_manager_and_tech_jury:
            message_value_html_template = render_to_string('nominate_app/emails/director_final_submission.html', \
                {'director_name':request.user.first_name, \
                    'name':recipient.username})
            plain_message_value = strip_tags(message_value_html_template)          
            send_mail(subject=subject_all, from_email='no-reply@pramati.com', \
                recipient_list=[str(recipient.email)], message=plain_message_value, fail_silently=False)        
        # to admin telling the process is complete
        subject_completion = "completion of the cycle"
        to_admin = User.objects.filter(groups__name='Admin')
        for admin in to_admin:
            message_value_html_template = render_to_string('nominate_app/emails/admins.html', \
                {'admin_name':admin.username})
            plain_message_value = strip_tags(message_value_html_template)          
            send_mail(subject=subject_completion, from_email='no-reply@pramati.com', \
                recipient_list=[str(admin.email)], message=plain_message_value, fail_silently=False)
        return redirect('nominate_app:approval')

    nomination_submitted = NominationSubmitted.objects.get(id=submission_id)
    ratings = NominationRating.objects.filter(submission_id=nomination_submitted.id)
    avg_rating = NominationRating.objects.filter(submission_id=submission_id).aggregate(Avg('rating'))['rating__avg']

    created = DirectorComments.objects.filter(nomination_submitted=nomination_submitted, user=request.user).exists()
    if created:
        comment = nomination_submitted.director_comment.first().comment
        status = nomination_submitted.get_status(nomination_submitted.status)
        return render(request, 'nominate_app/approvals/show.html', {'selected_nomination': nomination_submitted, 'avg_rating': avg_rating, 'ratings': ratings, 'status': status, 'comment': comment})    
        
    return render(request, 'nominate_app/approvals/new.html', {'selected_nomination': nomination_submitted, 'avg_rating': avg_rating, 'ratings': ratings})
