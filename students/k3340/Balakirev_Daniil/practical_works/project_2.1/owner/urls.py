from django.urls import path
from . import views

urlpatterns = [
    path('owner/<int:car_owner_pk>/', views.car_owner_detail, name='car_owner_detail'),
    path('owners/', views.all_car_owners, name='all_car_owners'),
    path('owner/create/', views.car_owner_create, name='car_owner_create'),
    path('cars/', views.AllCarsView.as_view(), name='all_cars'),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('cars/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update'),
    path('cars/create/', views.CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
]
