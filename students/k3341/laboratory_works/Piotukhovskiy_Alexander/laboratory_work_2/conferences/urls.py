from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.LogoutRedirectView.as_view(), name='logout_redirect'),
    path('', views.conference_list, name='conference_list'),
    path('conference/add/', views.create_conference, name='create_conference'),
    path('conference/<int:conference_id>/', views.conference_detail, name='conference_detail'),
    path('conference/<int:conference_id>/edit/', views.edit_conference, name='edit_conference'),
    path('conference/<int:conference_id>/delete/', views.delete_conference, name='delete_conference'),
    path('conference/<int:conference_id>/participants/', views.view_participants, name='view_participants'),
    path('conference/<int:conference_id>/rate/', views.rate_conference, name='rate_conference'),
    path('conference/<int:conference_id>/view_ratings/', views.view_ratings, name='view_ratings'),
    path('conference/<int:conference_id>/register/', views.register_for_conference, name='register_for_conference'),
    path('conference/<int:conference_id>/cancel/', views.cancel_registration, name='cancel_registration'),
    path('all-participants/', views.all_conference_participants, name='all_conference_participants'),
]
