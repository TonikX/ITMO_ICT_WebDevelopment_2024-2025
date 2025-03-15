from django.urls import path
from .views import *

urlpatterns = [
    path('owners/', OwnerListView.as_view(), name='owners_list'),
    path('owners/<int:pk>/', OwnerDetailView.as_view(), name='owner_detail'),
    path('owners/create/', OwnerCreateView.as_view(), name='owner_create'),
    path('owners/<int:pk>/update/', OwnerUpdateView.as_view(), name='owner_update'),
    path('owners/<int:pk>/delete/', OwnerDeleteView.as_view(), name='owner_delete'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/create/', CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
]
