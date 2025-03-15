from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register/', views.register),
    path('profile/', views.profile),
    path('logout/', views.logout_view),
    path('login/', views.login_view),
    path('my-races/', views.my_races),
    path('race/<race_id>', views.race)
]