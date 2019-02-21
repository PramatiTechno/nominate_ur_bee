from django.urls import path

from nominate_app.views import award_index,create_award_view

app_name = 'nominate_app'
urlpatterns = [  
	path('', award_index.home, name='home'),
	path('newawards/', create_award_view.awards, name='newawards'),
	path('view_awards/', award_index.view_awards, name='view_awards'),
	path('edit_awards/<award_id>', create_award_view.edit_awards, name='edit_awards'),
	path('award_template_index/', award_index.award_template_index, name='award_template_index'),
	path('award_template_load/<id>/', award_index.award_template_load, name='award_template_load'),
    path('delete/<nom_id>/', create_award_view.award_delete),
]
