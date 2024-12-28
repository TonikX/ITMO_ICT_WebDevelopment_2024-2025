from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import register

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('conference_list', views.conference_list, name='conference_list'),
    path('conference/<int:conference_id>/', views.conference_detail, name='conference_detail'),
    path('conference/<int:conference_id>/register/', views.register_for_conference, name='register_for_conference'),
    path('conference/<int:conference_id>/review/', views.add_review, name='add_review'),
    path('register/', views.register, name='register'),
    path('my_registrations/', views.my_registrations, name='my_registrations'),
    path('registration/<int:registration_id>/edit/', views.edit_registration, name='edit_registration'),
    path('registration/<int:registration_id>/delete/', views.delete_registration, name='delete_registration'),
    ]
