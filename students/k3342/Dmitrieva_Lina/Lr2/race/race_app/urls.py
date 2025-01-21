from django.urls import path
from . import views

urlpatterns = [
    path('racers/', views.racer_list, name='racers_list'),
    path('racers/<str:full_name>/', views.racer_details, name='racer_detail'),
    path('races/', views.race_list, name='race_list'),
    path('races/<str:name>/', views.race_detail, name='race_detail'),
    path('teams/<str:name>/', views.team_list, name='team_list'),
    path('racers/create/', views.create_racer, name='create_racer'),
    path('register/', views.register, name='register'),
]