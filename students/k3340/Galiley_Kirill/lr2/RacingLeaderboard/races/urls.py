from django.urls import path
from . import views

urlpatterns = [
    path('', views.race_list, name='race_list'),
    path('race/<int:pk>/', views.race_detail, name='race_detail'),
    path('race/<int:pk>/leaderboard/', views.race_leaderboard, name='race_leaderboard'),
    path('race/<int:race_id>/register/', views.register_for_race, name='register_race'),
    path('race/<int:race_id>/unregister/', views.unregister_from_race, name='unregister_race'),
    path('race/<int:race_id>/comment/', views.add_comment, name='add_comment'),

    path('drivers/', views.driver_list, name='driver_list'),
    path('driver/<int:pk>/', views.driver_detail, name='driver_detail'),
    path('driver/create/', views.create_driver_profile, name='create_driver_profile'),
    path('driver/<int:pk>/edit/', views.edit_driver_profile, name='edit_driver_profile'),

    path('teams/', views.team_list, name='team_list'),

    path('register/', views.register_user, name='register_user'),
]
