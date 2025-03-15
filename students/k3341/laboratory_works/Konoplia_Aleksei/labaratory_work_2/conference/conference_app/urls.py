from django.urls import path
from . import views
from .views import custom_logout

urlpatterns = [
    path('', views.home, name='home'),
    path('conference/<int:conference_id>/', views.conference_detail, name='conference_detail'),
    path('conference/<int:conference_id>/add_review/', views.add_review, name='add_review'),
    path('register/', views.user_register, name='user_register'),
    path('participants/', views.participants_table, name='participants_table'),
    path('registration/<int:reg_id>/edit/', views.edit_registration, name='edit_registration'),
    path('registration/<int:reg_id>/delete/', views.delete_registration, name='delete_registration'),
    path('accounts/logout/', custom_logout, name='logout'),
]
