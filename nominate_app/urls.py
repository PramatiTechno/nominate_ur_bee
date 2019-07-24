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
from nominate_app.views import awards,award_templates, award_template_views,nominate_process_view, nomination_status_view
from django.conf import settings 
from django.conf.urls.static import static

app_name = 'nominate_app'
urlpatterns = [
  path('', awards.index, name='home'),
  path("awards/",awards.index,name="awards"),
  path("awards/new/",awards.new,name="new_award"),
  path("awards/<award_id>/edit/",awards.edit,name="edit_award"),
  path('awards/<award_id>/', awards.award,name="award"),
  path('award_templates/', award_templates.home,name="award_templates_home"),
  path("awards/<award_id>/award_templates/",award_templates.index,name="award_templates_index"),
  path("awards/<award_id>/award_templates/new/",award_templates.new,name="new_template"),
  path("awards/<award_id>/award_templates/<award_template_id>/edit/",award_templates.edit,name="edit_award_template"),
  path('awards/<award_id>/award_templates/<award_template_id>/', award_templates.award_template,name="award_template"),
  path('question/delete/<ques_id>/', award_template_views.delete_award_template),
  path('nomination_status/', nomination_status_view.nomination_status, name='nomination_status'),
  path('nomination_status_load/<id>/', nomination_status_view.nomination_status_load, name='nomination_status_load'),
  path('manager_nominate_index/', nominate_process_view.manager_nominate_index, name='manager_nominate_index'),
  path('create_nomination/<chain_id>/', nominate_process_view.create_nomination, name='create_nomination'),
  path('view_nomination/<chain_id>/', nominate_process_view.view_nomination, name='view_nomination'),
  path('store_nomination/<nomination_instance_id>/', nominate_process_view.store_nomination, name='store_nomination'),
]

if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, 
document_root=settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL, 
document_root=settings.MEDIA_ROOT)