from django.contrib import admin
from django.urls import path
from project_first_app.views import CarListView, CarDetailView, CarCreateView, CarUpdateView, CarDeleteView, owner_list, add_owner, register

urlpatterns = [
    path('owners/', owner_list, name='owner_list'),
    path('owners/add/', add_owner, name='add_owner'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/add/', CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
    path('register/', register, name='register'),
]

