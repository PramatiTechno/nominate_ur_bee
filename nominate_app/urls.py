from django.urls import path

from nominate_app import award_index,create_award_view

app_name = 'nominate_app'
urlpatterns = [  
	path('', award_index.home, name='home'),
	path('view_awards/', award_index.view_awards, name='view_awards'),
	path('edit_awards/<id>', award_index.edit_awards, name='edit_awards'),
	path('award_template_index/', award_index.award_template_index, name='award_template_index'),
	path('award_template_load/<id>/', award_index.award_template_load, name='award_template_load'),
	path('newawards/', create_award_view.awards, name='newawards'),
    path('bee/<award_id>/', create_award_view.home, name='home'),
    path('bee/delete/<nom_id>/', create_award_view.award_delete),
]
