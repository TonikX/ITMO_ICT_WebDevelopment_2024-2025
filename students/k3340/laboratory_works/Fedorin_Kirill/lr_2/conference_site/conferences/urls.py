from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
       path('register/', views.register, name='register'),
       path('', views.conference_list, name='conference_list'),
       path('conference/<int:conference_id>/', views.conference_detail, name='conference_detail'),
       path('conference/<int:conference_id>/register/', views.register_for_conference, name='register_for_conference'),
       path('conference/<int:conference_id>/unregister/', views.unregister_from_conference, name='unregister_from_conference'),
       path('registration/edit/<int:registration_id>/', views.edit_registration, name='edit_registration'),
       path('registration/delete/<int:registration_id>/', views.delete_registration, name='delete_registration'),
       path('conference/<int:conference_id>/add_review/', views.add_review, name='add_review'),
       path('login/', auth_views.LoginView.as_view(template_name='conferences/login.html'), name='login'),
       path('logout/', auth_views.LogoutView.as_view(template_name='conferences/logout.html'), name='logout'),
   ]