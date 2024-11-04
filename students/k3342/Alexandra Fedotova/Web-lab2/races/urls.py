from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('participant_dashboard/', views.participant_dashboard, name='participant_dashboard'),
    path('profile_data/', views.profile_data, name='profile_data'),
    path('register_for_race/<int:race_id>/', views.register_for_race, name='register_for_race'),
    path('unregister_from_race/<int:registration_id>/', views.unregister_from_race, name='unregister_from_race'),
    path('races/', views.all_races, name='all_races'),
    path('race/<int:race_id>/results/', views.race_results, name='race_results'),
    path('race/<int:race_id>/registrations/', views.registrations_for_race, name='registrations_for_race'),
    path('add_comment/<int:race_id>/', views.add_comment, name='add_comment'),
    path('race_comments/<int:race_id>/', views.race_comments, name='race_comments'),
]
