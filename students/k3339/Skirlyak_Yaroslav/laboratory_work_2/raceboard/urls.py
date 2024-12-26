from django.urls import path
from . import views

urlpatterns = [
    path('', views.race_list, name='race_list'),
    path('register/', views.register, name='register'),
    path('races/', views.race_list, name='race_list'),
    path('races/<int:race_id>/', views.race_detail, name='race_detail'),
    path('races/<int:race_id>/register/', views.register_for_race, name='register_for_race'),
    path('races/<int:race_id>/comments/', views.add_comment, name='add_comment'),
    path('races/<int:race_id>/register/', views.register_for_race, name='register_for_race'),
    path('races/<int:race_id>/unregister/', views.unregister_from_race, name='unregister_from_race'),
    path('my_registrations/', views.my_registrations, name='my_registrations'),
    path('races/<int:race_id>/add_comment/', views.add_comment, name='add_comment'),
]
