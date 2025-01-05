from django.contrib.auth import views as auth_views
from django.urls import path
from .views import ConferenceListView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('conferences/', ConferenceListView.as_view(), name='conference_list'),
    path('conference/<int:conference_id>/', views.conference_detail, name='conference_detail'),
    path('conference/<int:conference_id>/register/', views.register_for_conference, name='register_for_conference'),
    path('conference/<int:conference_id>/review/', views.add_review, name='add_review'),
    path('participants/', views.participant_list, name='participant_list'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('conference/<int:conference_id>/edit_registration/', views.edit_registration, name='edit_registration'),
    path('conference/<int:conference_id>/delete_registration/', views.delete_registration, name='delete_registration'),
]

