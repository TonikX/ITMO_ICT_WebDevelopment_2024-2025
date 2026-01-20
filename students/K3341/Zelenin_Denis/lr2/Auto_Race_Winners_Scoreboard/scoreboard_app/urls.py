from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('user/<slug:user_slug>/', views.show_user, name ='show_user'),
    path('driver/<slug:driver_slug>/', views.show_driver, name='show_driver'),
    path('race/<int:race_id>/', views.detail_race, name='detail_race'),
    path('races/', views.show_races, name='races'),
    path('signup/', views.signup, name='signup'),
    path('', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('drivers/', views.show_drivers, name='drivers'),
    path('users/', views.show_users, name='users'),
    path('profile/', views.profile_view, name='profile'),
    path('adddrivers/', views.add_driver, name='add_driver'),
    path('addcar/', views.add_car, name='add_car'),
    path('addtruck/', views.add_truck, name='add_truck'),
    path('addrace/', views.add_race, name='add_race')


]
