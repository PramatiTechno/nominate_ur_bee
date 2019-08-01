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
from nominate_app.views import awards,award_templates, nomination_status_view,nomination_index,nominations,nomination_instances
from django.conf import settings 
from django.conf.urls.static import static

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
  path("nominations/",nominations.index,name="nominations"),
  path("nominations/<nomination_id>/nomination_instances/new/",nomination_instances.new,name="new_nomination_instance"),
  path("nominations/<nomination_id>/nomination_instances/",nomination_instances.index,name="create_nomination_instance"),
  path("nominations/<nomination_id>/nomination_instances/<nomination_instance_id>/edit/",nomination_instances.edit,name="edit_nomination_instance"),
  path("nominations/<nomination_id>/nomination_instances/<nomination_instance_id>/",nomination_instances.nomination_instance,name="nomination_instance"),


  path('nomination_status/', nomination_status_view.nomination_status, name='nomination_status'),
  path('nomination_status_load/<id>/', nomination_status_view.nomination_status_load, name='nomination_status_load'),
  path('nomination_feed/', nomination_index.NominationIndexView.as_view(), name='nomination_feed'),
  path('nomination_detail/<award_template_id>/', nomination_index.NominationDetailView.as_view(), name='nomination_detail'),
  path('nomination_detail/<award_template_id>/nomination_instance/<int:nomination_instance_id>/comment/', nomination_index.CommentList.as_view(), name='add_comment'),
  path('nomination_detail/<award_template_id>/nomination_instance/<int:nomination_instance_id>/comment/<int:comment_id>/delete', nomination_index.comment_remove, name='comment_remove'),
  path('nomination_detail/<award_template_id>/nomination_instance/<int:nomination_instance_id>/like/', nomination_index.nomination_like, name='nomination_like'),

  path('nomination_feed/nomination_instance/<int:nomination_instance_id>/comment/', nomination_index.CommentList.as_view(), name='add_comment'),
  path('nomination_feed/nomination_instance/<int:nomination_instance_id>/comment/<int:comment_id>/delete', nomination_index.comment_remove, name='comment_remove'),
  path('nomination_feed/nomination_instance/<int:nomination_instance_id>/like/', nomination_index.nomination_like, name='nomination_like'),

]

if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, 
document_root=settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL, 
document_root=settings.MEDIA_ROOT)