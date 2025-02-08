from django.urls import path
from .views import register
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('registrations/edit/<int:registration_id>/', views.edit_registration, name='edit_registration'),
    path('registrations/delete/<int:registration_id>/', views.delete_registration, name='delete_registration'),
    path('conferences/<int:conference_id>/add_review/', views.add_review, name='add_review'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('login/', auth_views.LoginView.as_view(next_page='index'), name='login'),
    path('my_registrations/', views.my_registrations_view, name='my_registrations'),
    path('edit_registration/<int:registration_id>/', views.edit_registration, name='edit_registration'),
    path('delete_registration/<int:registration_id>/', views.delete_registration, name='delete_registration'),
    path('conferences/register/', views.create_registration, name='create_registration'),
    path('reviews/', views.review_list, name='review_list'),
    path('conferences/', views.list_conferences),
    path('conferences/', views.list_conferences, name='list_conferences'),
    path('register/<int:conference_id>/', views.register_presentation),
    path('presentations/edit/<int:presentation_id>/', views.edit_presentation),
    path('presentations/delete/<int:presentation_id>/', views.delete_presentation),
    path('conferences/<int:conference_id>/add_review/', views.add_review, name='add_review'),
    path('conferences/<int:conference_id>/reviews/', views.review_list, name='review_list'),
]




    
