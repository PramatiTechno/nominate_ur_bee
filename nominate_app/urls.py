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
from nominate_app.views import award_template_views,award_index,create_award_view
from django.conf import settings 
from django.conf.urls.static import static

app_name = 'nominate_app'
urlpatterns = [
  path('', award_index.home, name='home'),
  path('newawards/', create_award_view.awards, name='newawards'),
  path('view_awards/', award_index.view_awards, name='view_awards'),
  path('edit_awards/<award_id>', create_award_view.edit_awards, name='edit_awards'),
  path('award_template_index/', award_index.award_template_index, name='award_template_index'),
  path('award_template_load/<id>/', award_index.award_template_load, name='award_template_load'),
  path('delete/<nom_id>/', create_award_view.award_delete),
  path('new_award_template/<award_id>/', award_template_views.new_award_template),
  path('edit_award_template/<template_id>/', award_template_views.edit_award_template),
  path('question/delete/<ques_id>/', award_template_views.delete_award_template),
]
