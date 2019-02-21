from django.urls import path
from nominate_app import create_award_view

urlpatterns = [
    # path('index/', create_award_view.home, name='index'),
    path('newawards/', create_award_view.awards, name='newawards'),
    path('bee/<award_id>/', create_award_view.home, name='home'),
    path('bee/delete/<nom_id>/', create_award_view.award_delete),
]
