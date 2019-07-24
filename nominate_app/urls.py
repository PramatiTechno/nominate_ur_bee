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
from nominate_app.views import award_template_views,award_index,create_award_view, nominate_process_view, nomination_status_view, nomination_index
from django.conf import settings 
from django.conf.urls.static import static

app_name = 'nominate_app'
urlpatterns = [
  path('', award_index.home, name='home'),
  path('newawards/', create_award_view.awards, name='newawards'),
  path('view_awards/', award_index.view_awards, name='view_awards'),
  path('edit_awards/<award_id>/', create_award_view.edit_awards, name='edit_awards'),
  path('award_template_index/', award_index.award_template_index, name='award_template_index'),
  path('award_template_load/<id>/', award_index.award_template_load, name='award_template_load'),
  path('delete/<nom_id>/', create_award_view.award_delete),
  path('new_award_template/<award_id>/', award_template_views.new_award_template, name='new_award_template'),
  path('edit_award_template/<template_id>/', award_template_views.edit_award_template, name='edit_award_template'),
  path('question/delete/<ques_id>/', award_template_views.delete_award_template),
  path('nomination_status/', nomination_status_view.nomination_status, name='nomination_status'),
  path('nomination_status_load/<id>/', nomination_status_view.nomination_status_load, name='nomination_status_load'),
  path('manager_nominate_index/', nominate_process_view.manager_nominate_index, name='manager_nominate_index'),
  path('create_nomination/<chain_id>/', nominate_process_view.create_nomination, name='create_nomination'),
  path('view_nomination/<chain_id>/', nominate_process_view.view_nomination, name='view_nomination'),
  path('store_nomination/<nomination_instance_id>/', nominate_process_view.store_nomination, name='store_nomination'),
  path('nomination_feed/', nomination_index.NominationIndexView.as_view(), name='nomination_feed'),
  path('nomination_detail/<award_template_id>/', nomination_index.NominationDetailView.as_view(), name='nomination_detail'),
  path('nomination_detail/<award_template_id>/nomination_instance/<int:nomination_instance_id>/add_comment/', nomination_index.CommentList.as_view(), name='add_comment'),

  path('nomination_instance/<int:instance_id>comment/<int:comment_id>/approve/', nomination_index.comment_approve, name='comment_approve'),
  path('nomination_instance/<int:instance_id>comment/<int:comment_id>/remove/', nomination_index.comment_remove, name='comment_remove'),
]

if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, 
document_root=settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL, 
document_root=settings.MEDIA_ROOT)