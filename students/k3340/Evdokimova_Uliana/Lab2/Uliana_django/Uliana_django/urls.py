"""
URL configuration for Uliana_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from project_first_app import views
from project_first_app.views import owner_list
from project_first_app.views import owner_list, CarListView, CarDetailView

urlpatterns = [

    path('owners/', owner_list, name='owner_list'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('owners/', owner_list, name='owner_list'),
    path('', views.home, name='home'),
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
    path('admin/', admin.site.urls),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.create_user, name='create_user'),
]




