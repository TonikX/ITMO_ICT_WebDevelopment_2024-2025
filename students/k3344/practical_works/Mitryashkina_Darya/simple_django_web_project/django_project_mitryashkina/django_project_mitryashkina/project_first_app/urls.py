from django.urls import path 
from . import views
from .views import CarsListView, CarDetailView, CreateCarView, UpdateCarView, DeleteCarView

urlpatterns = [
    path('owners/', views.owners, name='owners'),
    path('owners/<int:id>/', views.owner_info, name='owner_info'),
    path('owners/create/', views.create_owner, name='create_owner'),
    path('cars/', CarsListView.as_view(), name='cars'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_info'),
    path('cars/create/', CreateCarView.as_view(), name='create_car'),
    path('cars/update/<int:pk>/', UpdateCarView.as_view(), name='update_car'),
    path('cars/delete/<int:pk>/', DeleteCarView.as_view(), name='delete_car'),
]