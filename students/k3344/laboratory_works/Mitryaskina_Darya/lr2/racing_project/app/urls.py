from django.urls import path
from . import views
from .views import RaceList, RaceDetailes, ProfileList, DeleteRegistration

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', ProfileList.as_view(), name='profile'),
    path('profile/edit_registration/<int:registration_id>/', views.edit_registration, name='edit_registration'),
    path('profile/delete_registration/<int:pk>/', DeleteRegistration.as_view(), name='delete_registration'),
    path('races/', RaceList.as_view(), name='race_list'),
    path('races/<int:pk>', RaceDetailes.as_view(), name='race_detailes'),
    path('races/register_racer/<int:race_id>/', views.register_racer, name='register_racer'),
    path('races/add_comment/<int:race_id>/', views.add_comment, name='add_comment'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
]