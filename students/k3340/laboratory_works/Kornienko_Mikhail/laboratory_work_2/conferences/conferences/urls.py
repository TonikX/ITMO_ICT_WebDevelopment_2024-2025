from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.conferences_list, name='conf_list'),
    path('conferences/<int:conf_id>/presentations/', views.presentations_list, name='presentations_list'),
    path('registrations/<int:conf_id>/make_presentation/', views.make_presentation, name='make_presentation'),
    path('registrations/<int:conf_id>/enroll/', views.enroll, name='enroll'),
    path('registrations/', views.my_registrations, name='my_registrations'),
    path('registrations/<int:registration_id>/edit/', views.edit_registration, name='edit_registration'),
    path('registrations/<int:registration_id>/delete/', views.delete_registration, name='delete_registration'),
    path('registrations/<int:registration_id>/review/', views.add_review, name='add_review'),
    path('participants/', views.participants, name='participants'),
]
