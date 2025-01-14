from django.urls import path
from . import views
from .views import register, racer_list, delete_registration, race_list, \
    racer_detail, login_view, race_results, add_comment, race_detail

urlpatterns = [
    path('register/', register, name='register'),
    path('registration/<int:participant_id>/delete/', delete_registration, name='delete_registration'),
    path('login/', login_view, name='login'),
    path('racers/', racer_list, name='racer_list'),
    path('races/', race_list, name='race_list'),
    path('racers/<int:racer_id>/', racer_detail, name='racer_detail'),
    path('races/<int:race_id>/register/', views.race_registration, name='race_registration'),
    path('races/<int:race_id>/participants/', views.race_participants, name='race_participants'),
    path('races/<int:participant_id>/delete/', delete_registration, name='delete_registration'),
    path('races/<int:race_id>/results/', race_results, name='race_results'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile, name='profile'),
    path('races/<int:race_id>/', race_detail, name='race_detail'),
    path('races/<int:race_id>/participants/', views.race_participants, name='race_participants'),
    path('races/<int:race_id>/results/', views.race_results, name='race_results'),
    path('races/<int:race_id>/comments/add/', add_comment, name='add_comment'),
    path('races/<int:race_id>/comments/', views.race_comments, name='race_comments'),
    path('', views.racer_list, name='home'),
    path('races/', views.racer_list, name='race_list'),
    path('racers/', views.racer_list, name='racer_list'),
]
