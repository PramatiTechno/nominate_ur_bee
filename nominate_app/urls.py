from django.urls import path
from nominate_app import create_award_view

urlpatterns = [
    # path('home/', views.home, name='home'),
    # path('awards/', views.awards, name='awards'),
    path('bee/<award_id>/', create_award_view.home, name='home'),
    path('bee/delete/<nom_id>/', create_award_view.award_delete),
]
