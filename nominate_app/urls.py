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
from nominate_app import award_template_views 
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('new_award_template/<award_id>/', award_template_views.new_award_template),
    path('edit_award_template/<template_id>/', award_template_views.edit_award_template),
    path('new_home/', award_template_views.new_home, name='new_home'),
    path('question/delete/<ques_id>/', award_template_views.delete_award_template),
]
