"""
URL configuration for races project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from racestable import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path("registration/", views.registration, name="registration"),
    path("racer_registration/", views.racer_registration, name="racer_registration"),
    path("edit_user/", views.edit_user, name="edit_user"),
    path("change_password/", views.change_password, name="change_password"),
    path("edit_racer/", views.edit_racer, name="edit_racer"),
    path("races/comments/<int:race_id>/", views.race_comments, name="race_comments"),
    path("races/", views.races_list, name="races_list"),
    path("profile/delete/", views.delete_account, name="delete_account"),
    path("create_race_connection/<int:race_id>/", views.create_race_connection, name="create_race_connection"),
    path("delete_race_connection/<int:race_id>", views.delete_race_connection, name="delete_race_connection")
]
