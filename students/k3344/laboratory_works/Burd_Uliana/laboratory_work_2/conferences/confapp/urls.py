from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

app_name = 'confapp'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('conference/<int:conference_id>/', views.conference_detail, name='conference_detail'),
    path('home/', views.home, name='home'),
    path('my_registrations/', views.user_registrations, name='user_registrations'),
    path('registration/<int:registration_id>/edit/', views.edit_registration, name='edit_registration'),
    path('registration/<int:registration_id>/delete/', views.delete_registration, name='delete_registration'),
    path('conference/<int:conference_id>/register/', views.register_for_conference, name='register_for_conference'),
    path('conference/<int:conference_id>/edit/<int:registration_id>/', views.edit_registration, name='edit_registration'),
    path('conference/<int:conference_id>/participants/', views.conference_participants, name='conference_participants'),
    path('conference/<int:conference_id>/write_review/', views.write_review, name='write_review'),

]