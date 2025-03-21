"""
URL configuration for Lab_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from Conference.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', custom_login, name='login'),
    path('conferences/', conference_list, name='conference_list'),
    path('register/', register, name='register'),
    path('conference/<int:conference_id>/register/', register_for_presentation, name='register_presentation'),
    path('conference/<int:conference_id>/add_review/', add_review, name='add_review'),
    path('conferences/<int:conference_id>/', conference_detail, name='conference_detail'),
    path('profile/', profile, name='profile'),
    path('profile/presentation/edit/<int:presentation_id>/', edit_presentation, name='edit_presentation'),
    path('profile/presentation/delete/<int:presentation_id>/', delete_presentation, name='delete_presentation'),
]
