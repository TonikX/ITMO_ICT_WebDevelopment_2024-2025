from django.contrib import admin
from django.urls import path

from car_owners import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('owners/', views.owner_list, name='owner_list'),
    path('owners/create/', views.owner_create, name='owner_create'),
    path('owners/delete/<int:pk>/', views.owner_delete, name='owner_delete'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/create/<int:owner_id>/', views.car_create, name='car_create'),
    path('cars/delete/<int:pk>/', views.car_delete, name='car_delete'),
    path('licenses/', views.license_list, name='license_list'),
    path('licenses/create/<int:owner_id>/', views.license_create, name='license_create'),
    path('licenses/delete/<int:pk>/', views.license_delete, name='license_delete'),
    path('ownerships/', views.ownership_list, name='ownership_list'),
    path('ownerships/create/', views.ownership_create, name='ownership_create'),
    path('ownerships/delete/<int:pk>/', views.ownership_delete, name='ownership_delete'),
]
