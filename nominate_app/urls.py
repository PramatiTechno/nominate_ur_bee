"""nominate_your_bee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from nominate_app.views import awards,award_templates, nomination_status_view,nomination_index,nominations,nomination_instances, nomination_review, approvals, results, user_management, dashboard
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


app_name = 'nominate_app'
urlpatterns = [
  path("",awards.home, name='home'),
  path("awards/",awards.index,name="awards"),
  path("awards/new/",awards.new,name="new_award"),
  path("awards/<award_id>/edit/",awards.edit,name="edit_award"),
  path('awards/<award_id>/', awards.award,name="award"),
  path('award_templates/', award_templates.home,name="award_templates_home"),
  path("awards/<award_id>/award_templates/",award_templates.index,name="award_templates_index"),
  path("awards/<award_id>/award_templates/new/",award_templates.new,name="new_template"),
  path("awards/<award_id>/award_templates/<award_template_id>/edit/",award_templates.edit,name="edit_award_template"),
  path('awards/<award_id>/award_templates/<award_template_id>/', award_templates.award_template,name="award_template"),

  path("users/", user_management.index,name="users"),
  path("users/new", user_management.new,name="new_user"),
  path("users/create", user_management.create,name="create_user"),
  path("users/<user_id>/edit", user_management.edit_user,name="edit_user"),
  path("invited_users/<user_invite_id>/edit", user_management.edit_invite,name="edit_invited_user"),

  path("users/<user_id>/", user_management.user,name="user"),
  path("invited_users/<invited_user_id>/", user_management.invited_user,name="invited_user"),

  path("users/<user_id>/delete", user_management.delete_user,name="delete_user"),
  path("invited_users/<user_invite_id>/delete", user_management.delete_invite,name="delete_invited_user"),

  path("nominations/",nominations.index,name="nominations"),
  path('nominations/<status_value>', nominations.status_index, name="nomination_status_index"),
  path('nominations/submitted/<nomination_submitted_id>', nomination_instances.submitted_nomination, name="nomination_submitted"),
  path("nominations/<nomination_id>/",nominations.change_date,name="nominations_end_date"),
  path("nominations/<nomination_id>/nomination_instances/new/",nomination_instances.new,name="new_nomination_instance"),
  path("nominations/<nomination_id>/nomination_instances/",nomination_instances.index,name="create_nomination_instance"),
  path("nominations/<nomination_id>/nomination_instances/<nomination_instance_id>/edit/",nomination_instances.edit,name="edit_nomination_instance"),
  path("nominations/<nomination_id>/nomination_instances/<nomination_instance_id>/",nomination_instances.nomination_instance,name="nomination_instance"),   
  path("dashboard/",dashboard.index,name="dashboard"),      

  path("approvals/",approvals.index,name="approval"),
  path("approvals/<submission_id>",approvals.approve,name="approve"),    
  path("approvals/<submission_id>/edit",approvals.edit,name="approval_edit"),    

  path('nomination_status/', nomination_status_view.nomination_status, name='nomination_status'),
  
  path('nomination_feed/', nomination_index.NominationIndexView.as_view(), name='nomination_feed'),
  path('nomination_feed/<int:nomination_submittion_id>/', nomination_index.nomination_instance_post, name='nomination_instance_post'),
  path('nomination_feed/<int:nomination_submittion_id>/comment/', nomination_index.CommentList.as_view(), name='add_comment'),
  path('nomination_feed/<int:nomination_submittion_id>/comment/<int:comment_id>/delete', nomination_index.comment_remove, name='comment_remove'),
  path('nomination_feed/<int:nomination_submittion_id>/like/', nomination_index.nomination_like, name='nomination_like'),
  path('nomination_feed/<int:nomination_submittion_id>/liked_people/', nomination_index.nomination_liked_people, name='nomination_liked_people'),

  path('nomination_review/', nomination_review.index, name='nomination_review_index'),
  path('nomination_review/<int:nomination_submitted_id>', nomination_review.nomination_rating.as_view(), name='nomination_review_rating'),

  path('results/', results.index, name='results'),
  path('publish/<int:sub_id>/', results.publish, name='publish'),
  path('reemail/<username>/<int:nomination_id>/', nomination_status_view.email, name='reemail')
]

if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, 
document_root=settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL, 
document_root=settings.MEDIA_ROOT)